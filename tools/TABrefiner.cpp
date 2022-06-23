#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <cassert>
#include <algorithm>
#include <vector>
#include <map>
#include <tuple>
#include <set>
#include <getopt.h>

struct Config{
    std::string genome_size_file;
    std::string kraken_file;
    int max_depth;
    int min_depth;
    int read_length;
    float ldensity;
} config;

struct KrakenInfo{
    long long item_id ;
    bool    classify;
    std::string read_name ;
    std::string barcode;
    long long tax_id ;
    bool used ;

    static std::string get_barcode(const std::string & name) {
        std::string rt;
        bool b=false ;
        for(char c: name){
            if( c=='#' )
            {
                b=true;
                continue ;
            }
            else {
                if(b) rt+=c;
            }
        }
        return rt ;
    }

    void InitFromString(long long id , const std::string & line ) {
        item_id = id ;
        used = false ;
        std::istringstream ist(line);
        char c ;
        ist>>c>>read_name>>tax_id ;
        barcode = get_barcode(read_name);
        if(c == 'U')
            classify = false ;
        else if ( c== 'C' )
            classify = true ;
        else
        {
            classify =false;
            assert(0);
        }
    }
};

static long long all_zero = 0 ;
std::map<long long, std::vector<long long> > no_barcode_map ;
void AddNoBarcodeTax( long long id , long long rid ) {
    no_barcode_map[id].push_back(rid);
    all_zero ++ ;
}

struct Barcode {
    std::vector<long long> reads;
    std::map<long long, long long> assigned_reads ;
    bool used ;
    void incr_taxid(long long id ) {
        if( assigned_reads.find(id) == assigned_reads.end())
            assigned_reads[id] =1;
        else
            assigned_reads[id]+=1;
    }
};

struct Species {
    long long tax_id ;
    long long genome_size ;
    float depth ;
    std::vector<long long> reads;
    std::set<std::string> barcodes;
    void InitFromString(const std::string & line ){
        depth = 0;
        std::istringstream ist(line);
        ist>>tax_id>>genome_size;
    }
};

std::vector<KrakenInfo> reads_cache;
std::map<long long, Species> species ;
std::map<std::string , Barcode> barcodes ;

void LoadGenomes(const std::string file){
    std::ifstream ifs1(file) ;
    if( ! ifs1.is_open() ) {
        std::cerr<<"failed to open "<<file<<" for read! exit ..."<<std::endl;
        exit(1) ;
    }
    std::string  line ;
    while ( ! std::getline( ifs1 , line).eof() ){
        Species temp;
        temp.InitFromString(line);
        species[temp.tax_id]=temp;
    }
}

void LoadKraken(const std::string file){
    std::ifstream ifs1(file) ;
    if( ! ifs1.is_open() ) {
        std::cerr<<"failed to open "<<file<<" for read! exit ..."<<std::endl;
        exit(1) ;
    }
    std::string  line ;
    long long id = 0;;
    while ( ! std::getline( ifs1 , line).eof() ){
        KrakenInfo temp;
        temp.InitFromString(id ,line);
        reads_cache.push_back(temp);
        id ++ ;
    }
}

void OrganiseIds() {
    for( const auto & read : reads_cache ) {
        barcodes[read.barcode].used = false ;
        barcodes[read.barcode].reads.push_back(read.item_id);
        if( ! read.classify ) continue ;
        if( species.find(read.tax_id) == species.end() ) continue ;
        barcodes[read.barcode].incr_taxid(read.tax_id);
        species[read.tax_id].reads.push_back(read.item_id);
	// species only store valid barcode. 
        if( read.barcode == "0_0_0" || read.barcode == "0_0" )
            AddNoBarcodeTax(read.tax_id,read.item_id);
        else 
            species[read.tax_id].barcodes.insert(read.barcode);
    }
}

void ClacSpeciesDepth() {
    for(auto & one : species){
        long long sequences_size = 0 ;
        auto & one_item = one.second ;
        sequences_size = one_item.reads.size() * (config.read_length *2) ;
        one_item.depth = float(sequences_size)/float(one_item.genome_size);
    }
}
void PrintSpeciesDepth() {
    std::ofstream ost("tax_reads_depth.txt");
    if( ! ost.is_open() ) {
        std::cerr<<"failed to open tax_reads_depth.txt to write !! exit ..."<<std::endl;
        exit(1);
    }
    for(auto & one : species){
        auto & one_item = one.second ;
        ost<<one_item.tax_id<<'\t'<<one_item.reads.size()<<'\t'<<one_item.genome_size<<'\t'<<one_item.depth<<'\n';
    }
    ost.close();
}

//
//
//
//@return : last barcode
// 
std::string  Print_300X(const Species & one 
              ,const std::vector<std::tuple<long long,long long,std::string>> & barcode_infos 
              , bool all_read
              , bool x300){
    std::string last_barcode = "0_0_0";
    std::string tag;
    if( x300 ) tag = std::to_string(config.max_depth)+std::string("X.id_"); 
    else       tag = std::to_string(config.min_depth)+std::string("X.id_");
    std::string file_name = tag+std::to_string(one.tax_id);
    if(all_read)
        file_name +=".allread.txt" ;
    else
        file_name +=".allbarcode.txt" ;
    std::ofstream oft(file_name);
    if(! oft.is_open()) {
        std::cerr<<"failed to open "<<file_name<<" to write !! exit ..."<<std::endl;
        exit(1);
    }
    long long read_num = (one.genome_size) * config.max_depth / (config.read_length *2) ;
    long long printed_num = 0 ;
    std::vector<std::string> caches;
    // first print 0_0_0
    long long z_max = 0 ;
    if( all_read ) z_max = read_num/10 ;
    else z_max = read_num/20;

    const auto & zeros = no_barcode_map[one.tax_id];
    for( long long rid : zeros ) {
        auto & read = reads_cache.at(rid);
        caches.push_back(read.read_name);
        printed_num ++ ;
        if( printed_num >= z_max) 
            break;
    }
    // then print valid barcode
    for(const auto & tup : barcode_infos ) {
        long long barcode_reads , kraken_hit_reads ;
        std::string barcode ;
        std::tie( kraken_hit_reads ,barcode_reads, barcode ) = tup ;
        if( (float)kraken_hit_reads/ (float)barcode_reads<config.ldensity ) {
             continue ;
        }
        auto & barcode_item = barcodes.at(barcode);
        barcode_item.used = true ;
        for(long long id : barcode_item.reads ) {
            auto & read = reads_cache.at(id);
            if( ! all_read || ( all_read && read.classify && read.tax_id == one.tax_id ) ){
                caches.push_back(read.read_name);
                read.used=true;
            }
        }
	last_barcode = barcode;
        if(all_read)
            printed_num += kraken_hit_reads ;
        else
            printed_num += barcode_reads ;
        if( printed_num > read_num )
            break;
    }
    for( const auto & name : caches)
        oft<<name<<'\n';
    oft.close();
    return last_barcode;
}

void Print_species_info(long long id 
                 , const std::vector<std::tuple<long long ,long long,std::string>> & barcode_infos
                 , const std::string last_AB
                 , const std::string last_AR
){
    std::string file_name = std::string("tax_id.")+std::to_string(id)+".info.txt";
    std::ofstream oft(file_name);
    if(! oft.is_open()) {
        std::cerr<<"failed to open "<<file_name<<" to write !! exit ..."<<std::endl;
        exit(1);
    }
    const auto & zeros = no_barcode_map[id];
    long long ar_zero = zeros.size();
    oft<<"0_0_0\t"<<ar_zero<<" "<<all_zero<<" "<<float(ar_zero)/float(all_zero)<<" "<<"0_0_0"<<'\n';
    for(const auto & tup : barcode_infos ) {
        long long barcode_reads,kraken_hit_reads;
        std::string barcode ;
        std::tie( kraken_hit_reads,barcode_reads, barcode ) = tup ;
        oft<<barcode<<" "<<kraken_hit_reads<<" "<<barcode_reads<<" ";
        oft<<float(kraken_hit_reads)/float(barcode_reads)<<" "<<barcode;
	if( barcode == last_AB ) oft<<" last_AB";
	if( barcode == last_AR ) oft<<" last_AR";
        oft<<'\n';
    }
}

void Deal_major_species(){
    for(auto & one : species){
        auto & one_item = one.second ;
        if( one_item.depth < config.min_depth) continue ;
        bool x300 = true;
        if( one_item.depth < config.max_depth ) x300 = false ;
        std::vector<std::tuple<long long,long long,std::string>> barcode_infos ;
        for(const std::string &  b : one_item.barcodes ) {
            if( b == "0_0_0" || b == "0_0" ) continue ;
            const auto & barcode_item = barcodes.at(b);
            //                       kraken-hit-reads                                                 barcode-reads
            barcode_infos.push_back(std::make_tuple(barcode_item.assigned_reads.at(one_item.tax_id) ,(long long)(barcode_item.reads.size()) , b));
        }
        std::sort( barcode_infos.rbegin() ,  barcode_infos.rend() );
        std::string last_AR = Print_300X(one_item,barcode_infos,true , x300);
        std::string last_AB = Print_300X(one_item,barcode_infos,false, x300);
        Print_species_info(one_item.tax_id,barcode_infos,last_AB,last_AR);
    }
}

void Deal_left() {
    std::string file_name = std::string("others.ids.txt");
    std::ofstream oft(file_name);
    if(!oft.is_open()) {
        std::cerr<<"failed to open "<<file_name<<" to write !! exit ..."<<std::endl;
        exit(1);
    }
    std::vector<std::string> caches;
    for( const auto & read : reads_cache ) {
        if( read.used || read.barcode == "0_0_0" || read.barcode == "0_0" )
            continue ;
        auto & barcode_item = barcodes.at(read.barcode);
        if(barcode_item.used) continue ;
        caches.push_back(read.read_name);
    }
    for( const auto & name : caches)
        oft<<name<<'\n';
    oft.close();
}

void  printUsage(){
    std::cerr<<"TABrefiner <-g genome info file> <-k kraken result> [-r read_length default 100] [-m max output reads depth default 300 ]  [-n min output reads depth default 10 ] [-l kraken_hit_reads/barcode_reads threashold default 0 ]"<<std::endl;
    std::cerr<<std::endl;
}

int main(int argc , char ** argv ) {
    config.max_depth = 300;
    config.min_depth = 10 ;
    config.ldensity = 0 ;
    config.read_length=100;
    static struct option long_options[] = {
        {"genome_info",required_argument, NULL, 'g'},
        {"kraken_file",required_argument, NULL, 'k'},
        {"max_depth",required_argument,NULL, 'm'},
        {"min_depth",required_argument,NULL, 'n'},
        {"mdensity", required_argument,NULL, 'l'},
        {"read_length", required_argument,NULL, 'r'},
        {"help",  no_argument,       NULL, 'h'},
        {0, 0, 0, 0}
    };
    static char optstring[] = "g:k:m:n:l:r:h";
    while(1){
        int c = getopt_long(argc, argv, optstring, long_options, NULL);
        if (c<0) break;
        switch (c){
            case 'g':
                config.genome_size_file=std::string(optarg);
                break;
            case 'k':
                config.kraken_file = std::string(optarg);
                break;
            case 'm':
                config.max_depth=atoi(optarg);               
                break;
            case 'l':
                config.ldensity=atof(optarg);               
                break;
            case 'n':
                config.min_depth=atoi(optarg);               
                break;
            case 'r':
                config.read_length=atoi(optarg);
                break;
            case 'h':
                printUsage();
                return 0;
            default :
                printUsage();
                return -1;
        }
    }
    if( config.genome_size_file == "" || config.kraken_file == "" ) {
        printUsage();
        return -1 ;
    }

    //std::cerr<<KrakenInfo::get_barcode("CL100164780L1C001R003_100351#1177_1340_423")<<std::endl;
    LoadGenomes(config.genome_size_file);
    LoadKraken(config.kraken_file);
    OrganiseIds();
    ClacSpeciesDepth();
    PrintSpeciesDepth();

    Deal_major_species();
    Deal_left() ;

    return 0;
}

