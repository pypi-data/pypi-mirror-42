#ifndef PRIVACY_H_INCLUDED
#define PRIVACY_H_INCLUDED


#include <string>
#include <vector>
#include <map>
#include <utility>
#include <sstream>
#include <fstream>
#include <stdexcept>
#include <iostream>
#include <cstdio>
#include <algorithm>
#include <cstring>
#include <cmath>
#define INF 0x3f3f3f3f
#define MAT vector< vector<int> >
#define RES vector< vector<string> >
using namespace std;


// -+-+-+-+-+-+--+-+<support_function.h>-+-+-+-+-+-+-+-+-+-+


bool is_num(string str);


/*
 * convert string to integer
 */
int str2int(string str);


vector<string> str_split(string line);


/*
 * - check the flags to continue or not
 */
bool has_true_flag(vector<bool> flag);


int attr_value(int val);


string merge_result(int value1, int value2);


/*
 * - split the result 'a,b'
 *   attention: maybe pair.first is equal to pair.second
 */
pair<int, int> split_result(string attr);


string result_join(int value1, int value2);


string result_join(string value1, string value2);


// -+-+-+-+-+-+--+-+<io_class.h>-+-+-+-+-+-+-+-+-+-+


class Reader {
public:
    MAT data;
    vector<bool> is_str;
    vector< map<int, string> > inv_dict;


    Reader();


    /*
     * read file by line
     */
    RES get_raw_data(string filename);


    void check_input(int raw_data_dim, int QID_NUM, vector<int> QID_INDEX);
    void check_input(int raw_data_dim, int QID_NUM, vector<int> QID_INDEX, int SA_INDEX);


    /*
     * read file for 'K-Anonymity'
     * QID_NUM: the length of array QID_INDEX (eg. 3
     * QID_INDEX: the index of QID attributes in the file (eg. {0, 2, 3}
     */
    void read_k_anonymity(string filename, int QID_NUM, vector<int> QID_INDEX);


    /*
     * read file for 'L-Diversity'
     * QID_NUM: the length of array QID_INDEX (eg. 3
     * QID_INDEX: the index of QID attributes in the file (eg. {0, 2, 3}
     * SA_INDEX: the index of SA attribute(only one) (eg. 4
     */
    void read_l_diversity(string filename, int QID_NUM,
                          vector<int> QID_INDEX, int SA_INDEX);


    /*
     * read file for 'T-Closeness'
     * QID_NUM: the length of array QID_INDEX (eg. 3
     * QID_INDEX: the index of QID attributes in the file (eg. {0, 2, 3}
     * SA_INDEX: the index of SA attribute(only one) (eg. 4
     */
    void read_t_closeness(string filename, int QID_NUM,
                          vector<int> QID_INDEX, int SA_INDEX);


    /*
     * convert the int data to raw data(string)
     */
    RES convert_to_rawdata(RES data, vector<bool> is_str,
                           vector< map<int, string> > inv_dict);


    /*
     * write the results to file
     */
    void write_to_file(RES result, string filename);
};


// -+-+-+-+-+-+-+-+-+-+-+-<storage_class.h>+-+-+-+-+-+-+-+-+-+-+-+-+-+-


/*
 * 'Tetrad' represents four value group (1, 2, 3, 4)
 */
struct Tetrad {
    int split_value, next_value, low, high;

    Tetrad(int _sp_v, int ne_v, int _low, int _high);
};


/*
 * class 'KDTree' contains kd-tree partition info.
 * data: data in this node
 * low: low index of each QID (initial value is 0)
 * high: high index of each QID (initial value is len(data[dim]))
 * flag: 1 - can be divided on this dimension, 0 - can not.
 */
class KDTree {
public:
    MAT data;
    vector<int> low;
    vector<int> high;
    vector<bool> flag;

    KDTree();
    KDTree(const KDTree &kdt);
    KDTree(MAT _data, vector<int> _low,
           vector<int> _high, int qid_len);
    int get_len();
    void add_record(vector<int> record);
    void add_records(MAT records);
};


/*
 * (used in K-Anonymity)
 * class 'Qid' contains QID information in data (QID - "׼��ʶ������")
 * len: attributes in [0, len-1] are QID
 * val_list: unique & ordered value list for each qid
 * val_dict: {value: index} for each qid
 */
class Qid {
public:
    int len;
    MAT val_list;
    vector< map<int, int> > val_dict;

    Qid();
    int get_len();
    void data2qid(MAT data);
};


/*
 * (used in L-Diversity)
 * class 'FieldLD' contains QID & SA information
 * len: QID attributes' number (QID: data[0, len-1])
 * qid_list: QID[dim] -> unique & ordered value list
 * qid_dict: QID[dim] -> {value: index}
 * sa_value: SA value list (SA: data[len])
 */
class FieldLD {
public:
    int len;
    MAT qid_list;
    vector< map<int, int> > qid_dict;

    FieldLD();
    int get_len();
    void data2qid(MAT data);
};


/*
 * (used in T-Closeness)
 * class 'FieldTC' contains QID & SA information
 * len: QID attributes' number (QID: data[0, len-1])
 * qid_list: QID[dim] -> unique & ordered value list
 * qid_dict: QID[dim] -> {value: index}
 * sa_distribution: distribution of SA value (SA: data[len])
 */
class FieldTC: public FieldLD {
public:
    map<int, double> sa_distribution;

    FieldTC();
    void data2qid(MAT data);
};


// -+-+-+-+-+-+-+-+-+-+-+<k_anonymity.h>-+-+-+-+-+-+-+-+-+-+-+-+-+-+-


class K_Anonymity {
private:
    Qid QID;
    vector<KDTree> DIVIDE;

protected:
    /*
     * - find the best dimension to partition on this node "kd_tree",
     * by getting normalized distance of value in QID[dim]
     * attention: handle numeric data as well as string data
     */
    int find_split_dimension(KDTree kd_tree);

    /*
     * - find the middle value to split in 'dim' dimension of this node 'kd_tree'
     * attention: handle numeric data as well as string data
     */
    Tetrad find_split_value(KDTree kd_tree, int k, int dim);

    /*
     * - check the condition
     */
    bool check_k_anonymity(KDTree kd_tree, int k);


    /*
     * - partition on kd-tree node recursively
     * kd_tree: 'KDTree' node
     * k: the parameter k for k-anonymity
     */
    void my_partition(KDTree kd_tree, int k);


public:
    /*
     * - The main function of K-Anonymity
     * data: dataset in 2-dimensional array
     * k: the parameter k for k-anonymity
     */
    RES get_result(MAT data, int k);

};


void k_anonymity(string infile, int QID_NUM, vector<int> QID_INDEX, int k, string outfile);


// -+-+-+-+-+-+-+-+-+-+-+<l_diversity.h>-+-+-+-+-+-+-+-+-+-+-+-+-+-+-


class L_Diversity {
private:
    FieldLD FIELD;
    vector<KDTree> DIVIDE;

protected:
    int find_split_dimension(KDTree kd_tree);
    Tetrad find_split_value(KDTree kd_tree, int dim);
    bool check_l_diversity(KDTree kd_tree, int l);
    void my_partition(KDTree kd_tree, int l);

public:
    RES get_result(MAT data, int l);

};


void l_diversity(string infile, int QID_NUM, vector<int> QID_INDEX,
                 int SA_INDEX, int l, string outfile);


// -+-+-+-+-+-+-+-+-+-+-+<t_closeness.h>-+-+-+-+-+-+-+-+-+-+-+-+-+-+-


class T_Closeness {
private:
    FieldTC FIELD;
    vector<KDTree> DIVIDE;

protected:
    int find_split_dimension(KDTree kd_tree);
    Tetrad find_split_value(KDTree kd_tree, int dim);
    bool check_t_closeness(KDTree kd_tree, double t);
    void my_partition(KDTree kd_tree, double t);

public:
    RES get_result(MAT data, double t);

};


void t_closeness(string infile, int QID_NUM, vector<int> QID_INDEX,
                 int SA_INDEX, double t, string outfile);


#endif // PRIVACY_H_INCLUDED
