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
        sequences_size = one_item.reads.size() * 200 ;
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

void Print_300X(const Species & one ,const std::vector<std::tuple<long long,long long,std::string>> & barcode_infos , bool all_read, bool x300){
    std::string tag;
    if( x300 ) tag = std::string("300X.id_"); 
    else       tag = std::string("10X.id_");
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
    long long read_num = (one.genome_size) * 300 / 200 ;
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
        long long total_read , ar_read ;
        std::string barcode ;
        std::tie( ar_read ,total_read, barcode ) = tup ;
        auto & barcode_item = barcodes.at(barcode);
        barcode_item.used = true ;
        for(long long id : barcode_item.reads ) {
            auto & read = reads_cache.at(id);
            if( ! all_read || ( all_read && read.classify && read.tax_id == one.tax_id ) ){
                caches.push_back(read.read_name);
                read.used=true;
            }
        }
        if(all_read)
            printed_num += ar_read ;
        else
            printed_num += total_read ;
        if( printed_num > read_num )
            break;
    }
    for( const auto & name : caches)
        oft<<name<<'\n';
    oft.close();
}

void Print_species_info(long long id , const std::vector<std::tuple<long long ,long long,std::string>> & barcode_infos){
    std::string file_name = std::string("tax_id.")+std::to_string(id)+".info.txt";
    std::ofstream oft(file_name);
    if(! oft.is_open()) {
        std::cerr<<"failed to open "<<file_name<<" to write !! exit ..."<<std::endl;
        exit(1);
    }
    const auto & zeros = no_barcode_map[id];
    long long ar_zero = zeros.size();
    oft<<"0_0_0"<<ar_zero<<" "<<all_zero<<" "<<float(ar_zero)/float(all_zero)<<" "<<"0_0_0"<<'\n';
    for(const auto & tup : barcode_infos ) {
        long long total_read , ar_read ;
        std::string barcode ;
        std::tie( ar_read ,total_read, barcode ) = tup ;
        oft<<barcode<<" "<<ar_read<<" "<<total_read<<" "<<float(ar_read)/float(total_read)<<" "<<barcode<<'\n';
    }
}

void Deal_major_species(){
    for(auto & one : species){
        auto & one_item = one.second ;
        if( one_item.depth < 10) continue ;
        bool x300 = true;
        if( one_item.depth < 300 ) x300 = false ;
        std::vector<std::tuple<long long,long long,std::string>> barcode_infos ;
        for(const std::string &  b : one_item.barcodes ) {
            if( b == "0_0_0" || b == "0_0" ) continue ;
            const auto & barcode_item = barcodes.at(b);
            barcode_infos.push_back(std::make_tuple(barcode_item.assigned_reads.at(one_item.tax_id) ,(long long)(barcode_item.reads.size()) , b));
        }
        std::sort( barcode_infos.rbegin() ,  barcode_infos.rend() );
        Print_species_info(one_item.tax_id,barcode_infos);
        Print_300X(one_item,barcode_infos,true , x300);
        Print_300X(one_item,barcode_infos,false, x300);
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

int main(int argc , char ** argv ) {
    if ( argc != 3 ) {
        std::cerr<<"Usage : SplitSpecies genome_size.txt  kranken.txt"<<std::endl;
        return 1;
    }
    std::cerr<<KrakenInfo::get_barcode("CL100164780L1C001R003_100351#1177_1340_423")<<std::endl;
    std::string genome_size_file = std::string(argv[1]);
    std::string kraken_file = std::string(argv[2]);
    LoadGenomes(genome_size_file);
    LoadKraken(kraken_file);
    OrganiseIds();
    ClacSpeciesDepth();
    PrintSpeciesDepth();

    Deal_major_species();
    Deal_left() ;

    return 0;
}

