#include "privacy.h"


// -+-+-+-+-+-+--+-+<support_function.cpp>-+-+-+-+-+-+-+-+-+-+


bool is_num(string str) {
    stringstream ss(str);
    int d;
    char c;
    if (!(ss >> d)) {
        return false;
    }
    if (ss >> c) {
        return false;
    }
    return true;
}


int str2int(string str) {
    int res;
    stringstream ss(str);
    ss >> res;
    return res;
}


vector<string> str_split(string line) {
    vector<string> new_line;
    char *s = (char *)line.c_str();
    const char *sep = ",\t ;/|-+";
    char *p;
    p = strtok(s, sep);
    while(p) {
        new_line.push_back(string(p));
        p = strtok(NULL, sep);
    }
    return new_line;
}


bool has_true_flag(vector<bool> flag) {
    vector<bool>::iterator iter;
    for (iter=flag.begin(); iter!=flag.end(); iter++) {
        if (*iter == true) {
            return true;
        }
    }
    return false;
}


int attr_value(int val) {
    return val;
}


string merge_result(int value1, int value2) {
    stringstream s1, s2;
    s1 << value1, s2 << value2;
    string result, v1(s1.str()), v2(s2.str());
    if (value1 == value2) {
        result = "" + v1;
    } else {
        result = "" + v1 + "," + v2;
    }
    return result;
}


pair<int, int> split_result(string attr) {
    pair<int, int> attr_pair;
    vector<string> attr_list = str_split(attr);
    attr_pair.first = str2int(attr_list[0]);
    attr_pair.second = str2int(attr_list.back());
    return attr_pair;
}


string result_join(int value1, int value2) {
    stringstream s1, s2;
    s1 << value1, s2 << value2;
    string result, v1(s1.str()), v2(s2.str());
    if (value1 == value2) {
        result = "[" + v1 + "]";
    } else {
        result = "[" + v1 + ", " + v2 + "]";
    }
    return result;
}


string result_join(string value1, string value2) {
    string result;
    if (value1 == value2) {
        result = "[" + value1 + "]";
    } else {
        result = "[" + value1 + ", " + value2 + "]";
    }
    return result;
}


// -+-+-+-+-+-+--+-+<io_class.cpp>-+-+-+-+-+-+-+-+-+-+


Reader::Reader() {}


RES Reader::get_raw_data(string filename) {
    ifstream infile(filename.c_str());
    if (infile.fail()) {
        throw invalid_argument("Error: File not found!");
    }
    RES raw_data;
    string line;
    while (getline(infile, line)) {
        // case 1: blank line..
        if (line == "" || line == " " || line == "\n") {
            continue;
        }
        // case 2: remove enter character at the end of line..
        int len = line.size();
        if (line[len-1] == '\n') {
            line.erase(line.end()-1);
        }
        // split the string (using strtok function)
        vector<string> new_line = str_split(line);
        raw_data.push_back(new_line);
    }
    infile.close();
    return raw_data;
}


void Reader::check_input(int raw_data_dim, int QID_NUM, vector<int> QID_INDEX) {
    if (QID_NUM < 0 || QID_NUM > raw_data_dim) {
        throw invalid_argument("Error: QID_NUM can't be smaller than 0 or larger than the number of attributes!");
    }
    if (QID_NUM != QID_INDEX.size()) {
        throw invalid_argument("Error: QID_NUM is not match QID_INDEX!");
    }
    vector<int>::iterator iter;
    int dim = 0;
    for (iter=QID_INDEX.begin(); iter!=QID_INDEX.end(); iter++) {
        if (QID_INDEX[dim] < 0 || QID_INDEX[dim] > raw_data_dim-1) {
            throw invalid_argument("Error: Elements in QID_INDEX can't be smaller than 0 or larger than the number of attributes!");
        }
        dim++;
    }
}


void Reader::check_input(int raw_data_dim, int QID_NUM, vector<int> QID_INDEX, int SA_INDEX) {
    check_input(raw_data_dim, QID_NUM, QID_INDEX);
    if (SA_INDEX < 0 || SA_INDEX > raw_data_dim-1) {
        throw invalid_argument("Error: SA_INDEX is out of range!");
    }
    vector<int>::iterator iter;
    int dim = 0;
    for (iter=QID_INDEX.begin(); iter!=QID_INDEX.end(); iter++) {
        if (SA_INDEX == QID_INDEX[dim]) {
            throw invalid_argument("Error: SA_INDEX should not occur in QID_INDEX!");
        }
        dim++;
    }
}


void Reader::read_k_anonymity(string filename, int QID_NUM, vector<int> QID_INDEX) {
    // get raw data
    RES raw_data = get_raw_data(filename);
    // check user's input arguments
    check_input(raw_data[0].size(), QID_NUM, QID_INDEX);
    // init the inverted index
    vector<int> attr_cnt;
    vector< map<string, int> > attr_dict;
    map<int, string> _dict;
    map<string, int> dict;
    map<string, int>::iterator iter_find;
    for (int i = 0; i < QID_NUM; i++) {
        attr_cnt.push_back(0);
    }
    for (int i = 0; i < QID_NUM; i++) {
        attr_dict.push_back(dict);
        inv_dict.push_back(_dict);
    }
    // get 'int' data through raw_data
    RES::iterator iter;
    vector<string> raw_record;
    vector<int> record;
    string val;
    bool flag = true;  // judge attribute is numerical or string in the first line.
    for (iter = raw_data.begin(); iter != raw_data.end(); iter++) {
        raw_record = *iter;
        record.clear();
        for (int i = 0; i < QID_NUM; i++) {
            val = raw_record[QID_INDEX[i]];
            if (is_num(val)) {             // numerical data.
                record.push_back(str2int(val));
                if (flag) {
                    is_str.push_back(false);
                }
            } else {                       // string data. (using inverted index..)
                iter_find = attr_dict[i].find(val);
                if (iter_find == attr_dict[i].end()) {
                    attr_dict[i][val] = attr_cnt[i];
                    inv_dict[i][attr_cnt[i]] = val;
                    attr_cnt[i]++;
                }
                record.push_back(attr_dict[i][val]);
                if (flag) {
                    is_str.push_back(true);
                }
            }
        }
        data.push_back(record);
        flag = false;
    }
}


void Reader::read_l_diversity(string filename, int QID_NUM,
                              vector<int> QID_INDEX, int SA_INDEX) {
    // get raw data
    RES raw_data = get_raw_data(filename);
    // check user's input arguments
    check_input(raw_data[0].size(), QID_NUM, QID_INDEX, SA_INDEX);
    // init the inverted index
    vector<int> attr_cnt;
    vector< map<string, int> > attr_dict;
    map<int, string> _dict;
    map<string, int> dict;
    map<string, int>::iterator iter_find;
    for (int i = 0; i < QID_NUM+1; i++) {     // differ from 'read_k_anonymity'
        attr_cnt.push_back(0);
    }
    for (int i = 0; i < QID_NUM+1; i++) {     // differ from 'read_k_anonymity'
        attr_dict.push_back(dict);
        inv_dict.push_back(_dict);
    }
    // get 'int' data through raw_data
    RES::iterator iter;
    vector<string> raw_record;
    vector<int> record;
    string val;
    bool flag = true;  // judge attribute is numerical or string in the first line.
    for (iter = raw_data.begin(); iter != raw_data.end(); iter++) {
        raw_record = *iter;
        record.clear();
        for (int i = 0; i < QID_NUM; i++) {
            val = raw_record[QID_INDEX[i]];
            if (is_num(val)) {             // numerical data.
                record.push_back(str2int(val));
                if (flag) {
                    is_str.push_back(false);
                }
            } else {                       // string data. (using inverted index..)
                iter_find = attr_dict[i].find(val);
                if (iter_find == attr_dict[i].end()) {
                    attr_dict[i][val] = attr_cnt[i];
                    inv_dict[i][attr_cnt[i]] = val;
                    attr_cnt[i]++;
                }
                record.push_back(attr_dict[i][val]);
                if (flag) {
                    is_str.push_back(true);
                }
            }
        }
        val = raw_record[SA_INDEX];
        if (is_num(val)) {
            record.push_back(str2int(val));
        } else {
            iter_find = attr_dict[QID_NUM].find(val);
            if (iter_find == attr_dict[QID_NUM].end()) {
                attr_dict[QID_NUM][val] = attr_cnt[QID_NUM];
                inv_dict[QID_NUM][attr_cnt[QID_NUM]] = val;
                attr_cnt[QID_NUM]++;
            }
            record.push_back(attr_dict[QID_NUM][val]);
        }
        data.push_back(record);
        flag = false;
    }
}


void Reader::read_t_closeness(string filename, int QID_NUM,
                              vector<int> QID_INDEX, int SA_INDEX) {
    read_l_diversity(filename, QID_NUM, QID_INDEX, SA_INDEX);
}


RES Reader::convert_to_rawdata(RES data, vector<bool> is_str,
                               vector< map<int, string> > inv_dict) {
    RES::iterator iter;
    vector<string> record;
    vector<string>::iterator iter2;
    string attr;
    pair<int, int> attr_pair;
    int a, b, qid_len = is_str.size();
    string left, right;
    RES result;
    vector<string> new_record;
    for (iter=data.begin(); iter!=data.end(); iter++) {
        record = *iter;
        new_record.clear();
        int dim = 0;
        for (iter2=record.begin(); iter2!=record.end(); iter2++) {
            attr = *iter2;
            attr_pair = split_result(attr);
            a = attr_pair.first;
            b = attr_pair.second;
            if (is_str[dim]) {           // this qid[dim] is string data
                left = inv_dict[dim][a];
                right = inv_dict[dim][b];
                new_record.push_back(result_join(left, right));
            } else {                     // qid[dim] is numerical data.
                new_record.push_back(result_join(a, b));
            }
            dim++;
        }
        result.push_back(new_record);
    }
    return result;
}


void Reader::write_to_file(RES result, string filename) {
    ofstream outfile(filename.c_str());
    RES::iterator iter;
    vector<string> r;
    vector<string>::iterator iter2;
    string line;
    for (iter = result.begin(); iter != result.end(); iter++) {
        r = *iter;
        line = "";
        for (iter2 = r.begin(); iter2 != r.end(); iter2++) {
            line += *iter2;
            line += "\t";
        }
        line += "\n";
        // write to file by line..
        outfile << line;
    }
    outfile.close();
}


// -+-+-+-+-+-+-+-+-+-+-+-<storage_class.cpp>+-+-+-+-+-+-+-+-+-+-+-+-+-+-


Tetrad::Tetrad(int _sp_v, int ne_v, int _low, int _high) {
    split_value = _sp_v;
    next_value = ne_v;
    low = _low;
    high = _high;
}


KDTree::KDTree() {}


KDTree::KDTree(const KDTree &kdt) {
    data = kdt.data;
    low = kdt.low;
    high = kdt.high;
    flag = kdt.flag;
}


KDTree::KDTree(MAT _data, vector<int> _low, vector<int> _high, int qid_len) {
    data = _data;
    low = _low;
    high = _high;
    vector<bool>::iterator ite = flag.begin();
    flag.insert(ite, qid_len, true);
}


int KDTree::get_len() {
    return data.size();
}


void KDTree::add_record(vector<int> record) {
    data.push_back(record);
}


void KDTree::add_records(MAT records) {
    MAT::iterator iter;
    for (iter=records.begin(); iter!=records.end(); iter++) {
        add_record(*iter);
    }
}


Qid::Qid() {}


int Qid::get_len() {
    return len;
}

void Qid::data2qid(MAT data) {
    len = data[0].size();
    MAT::iterator iter;
    vector<int> attr_val, tmp;
    vector<int>::iterator iter2;
    map<int, int> val_idx;
    for (int dim = 0; dim < len; dim++) {
        // get unique & ordered value in each dimension of qid
        attr_val.clear();
        for (iter=data.begin(); iter!=data.end(); iter++) {
            tmp = *iter;
            attr_val.push_back(tmp[dim]);
        }
        sort(attr_val.begin(), attr_val.end());
        iter2 = unique(attr_val.begin(), attr_val.end());
        attr_val.erase(iter2, attr_val.end());
        val_list.push_back(attr_val);

        // in each val_dict[dim], get the dictionary {value: index}
        val_idx.clear();
        int index = 0;
        for (iter2=attr_val.begin(); iter2!=attr_val.end(); iter2++) {
            int value = attr_val[index];
            val_idx[value] = index;
            index++;
        }
        val_dict.push_back(val_idx);
    }
}


FieldLD::FieldLD() {}


int FieldLD::get_len() {
    return len;
}


void FieldLD::data2qid(MAT data) {
    len = data[0].size() - 1;                 // differ from Qid class
    MAT::iterator iter;
    vector<int> attr_val, tmp;
    vector<int>::iterator iter2;
    map<int, int> val_idx;
    for (int dim = 0; dim < len; dim++) {
        // get unique & ordered value in each dimension of qid
        attr_val.clear();
        for (iter=data.begin(); iter!=data.end(); iter++) {
            tmp = *iter;
            attr_val.push_back(tmp[dim]);
        }
        sort(attr_val.begin(), attr_val.end());
        iter2 = unique(attr_val.begin(), attr_val.end());
        attr_val.erase(iter2, attr_val.end());
        qid_list.push_back(attr_val);

        // in each val_dict[dim], get the dictionary {value: index}
        val_idx.clear();
        int index = 0;
        for (iter2=attr_val.begin(); iter2!=attr_val.end(); iter2++) {
            int value = attr_val[index];
            val_idx[value] = index;
            index++;
        }
        qid_dict.push_back(val_idx);
    }
}


FieldTC::FieldTC() {}


void FieldTC::data2qid(MAT data) {
    len = data[0].size() - 1;                 // differ from Qid class
    MAT::iterator iter;
    vector<int> attr_val, tmp;
    vector<int>::iterator iter2;
    map<int, int> val_idx;
    for (int dim = 0; dim < len; dim++) {
        // get unique & ordered value in each dimension of qid
        attr_val.clear();
        for (iter=data.begin(); iter!=data.end(); iter++) {
            tmp = *iter;
            attr_val.push_back(tmp[dim]);
        }
        sort(attr_val.begin(), attr_val.end());
        iter2 = unique(attr_val.begin(), attr_val.end());
        attr_val.erase(iter2, attr_val.end());
        qid_list.push_back(attr_val);

        // in each val_dict[dim], get the dictionary {value: index}
        val_idx.clear();
        int index = 0;
        for (iter2=attr_val.begin(); iter2!=attr_val.end(); iter2++) {
            int value = attr_val[index];
            val_idx[value] = index;
            index++;
        }
        qid_dict.push_back(val_idx);
    }

    // get distribution of SA value (the last column in data)
    int sa_cnt = data.size();// sa_cnt is equal to records number
    map<int, double>::iterator ite_find;
    for (int i = 0; i < sa_cnt; i++) {
        vector<int> record = data[i];
        vector<int>::iterator ite = record.end() - 1;
        int sa_value = *ite;
        ite_find = sa_distribution.find(sa_value);
        if (ite_find != sa_distribution.end()) {
            sa_distribution[sa_value] += 1.0 / sa_cnt;
        } else {
            sa_distribution[sa_value] = 1.0 / sa_cnt;
        }
    }
}


// -+-+-+-+-+-+-+-+-+-+-+<k_anonymity.cpp>-+-+-+-+-+-+-+-+-+-+-+-+-+-+-


int K_Anonymity::find_split_dimension(KDTree kd_tree) {
    int max_dim = -1;
    double max_dis = -1;
    for (int dim = 0; dim < QID.get_len(); dim++) {
        if (!kd_tree.flag[dim]) {
            continue;
        }
        vector<int> dim_list = QID.val_list[dim];
        int value_range = attr_value(dim_list[kd_tree.high[dim]]) -
                          attr_value(dim_list[kd_tree.low[dim]]);
        int total_range = dim_list[dim_list.size()-1] - dim_list[0];
        double dis = (double)value_range / total_range;
        if (dis > max_dis) {
            max_dis = dis;
            max_dim = dim;
        }
    }
    return max_dim;
}


Tetrad K_Anonymity::find_split_value(KDTree kd_tree, int k, int dim) {
    // count number of each different value in each dimension
    map<int, int> value_count;          // (value -> cnt) dictionary for kd_tree.data[:, dim]
    vector<int> value_list;             // (value) list [unique/ascend] for kd_tree.data[:, dim]
    MAT::iterator iter;
    vector<int> record;
    map<int, int>::iterator iter_find;
    for (iter=kd_tree.data.begin(); iter!=kd_tree.data.end(); iter++) {
        record = *iter;
        iter_find = value_count.find(record[dim]);
        if (iter_find != value_count.end()) {
            value_count[record[dim]] += 1;
        } else {
            value_count[record[dim]] = 1;
            value_list.push_back(record[dim]);
        }
    }
    // get unique & ordered value in the given dimension of data
    sort(value_list.begin(), value_list.end());

    // cann't divide anymore(less than k) or there is only one different value
    int mid_count = kd_tree.data.size() / 2;
    if (mid_count < k || value_list.size() <= 1) {
        if (value_list.size() > 0) {
            return Tetrad(-INF, -INF, value_list[0], value_list.back());
        }
        return Tetrad(-INF, -INF, -INF, -INF);
    }

    // find the split value & index (median)
    int cnt = 0, split_index = 0, value, split_value, next_value;
    for (int i = 0; i < value_list.size(); i++) {
        value = value_list[i];
        cnt += value_count[value];
        if (cnt >= mid_count) {
            split_value = value;
            split_index = i;
            break;
        }
    }
    // get the value behind the split_val
    if (split_index + 1 < value_list.size()) {
        next_value = value_list[split_index + 1];
    } else {
        next_value = split_value;
    }
    return Tetrad(split_value, next_value, value_list[0], value_list.back());
}


bool K_Anonymity::check_k_anonymity(KDTree kd_tree, int k) {
    if (kd_tree.data.size() < k) {
        return false;
    }
    return true;
}


void K_Anonymity::my_partition(KDTree kd_tree, int k) {
    // terminal condition: can not split anymore..
    if (!has_true_flag(kd_tree.flag)) {
        DIVIDE.push_back(kd_tree);
        return;
    }

    // choose split attribute
    int dim = find_split_dimension(kd_tree);
    // special case: can not choose any dimension
    if (dim == -1) {
        DIVIDE.push_back(kd_tree);
        return;
    }

    // choose split value
    Tetrad t = find_split_value(kd_tree, k, dim);
    int split_value = t.split_value, next_value = t.next_value;
    int low = t.low, high = t.high;
    // update low and high bound of this node
    if (low != -INF) {
        kd_tree.low[dim] = QID.val_dict[dim][low];
        kd_tree.high[dim] = QID.val_dict[dim][high];
    }
    // special case: cannot split -> try to find next best dimension
    if (split_value == -INF) {
        kd_tree.flag[dim] = false;
        my_partition(kd_tree, k);
        return;
    }
//    printf("dim: %d, split_val: %d\n", dim, split_value);

    // build the left-child & right-child
    int split_index = QID.val_dict[dim][split_value];
    vector<int> lnode_high = kd_tree.high;
    lnode_high[dim] = split_index;
    vector<int> rnode_low = kd_tree.low;
    rnode_low[dim] = QID.val_dict[dim][next_value];
    MAT sub_data;
    sub_data.clear();
    KDTree lnode = KDTree(sub_data, kd_tree.low, lnode_high, QID.get_len());
    KDTree rnode = KDTree(sub_data, rnode_low, kd_tree.high, QID.get_len());
    // judge the data in this node belong to left-child or right-child
    MAT mid_set;
    vector<int> record;
    MAT::iterator iter;
    for (iter=kd_tree.data.begin(); iter!=kd_tree.data.end(); iter++) {
        record = *iter;
        int idx = QID.val_dict[dim][record[dim]];
        if (idx < split_index) {
            lnode.add_record(record);
        } else if (idx > split_index) {
            rnode.add_record(record);
        } else {
            mid_set.push_back(record);
        }
    }
    // attention: handle records which equal to record[split_index]
    int half_len = kd_tree.get_len() / 2;
    for (int i = 0; i < (half_len-lnode.get_len()); i++) {
        record = mid_set.back();
        mid_set.pop_back();
        lnode.add_record(record);
    }
    if (mid_set.size() > 0) {                    // there are extra multiple records..
        rnode.low[dim] = split_index;
        rnode.add_records(mid_set);
    }

    // anonymize sub-partition
    // try to split this node only when lnode & rnode satisfy conditions
//    printf("dim: %d -> (%d / %d)\n", dim, lnode.data.size(), rnode.data.size());
    if (!check_k_anonymity(lnode, k) || !check_k_anonymity(rnode, k)) {
        DIVIDE.push_back(kd_tree);
        return;
    }
//    printf("dim: %d -> [%d / %d]\n", dim, lnode.data.size(), rnode.data.size());
    my_partition(lnode, k);
    my_partition(rnode, k);
}


RES K_Anonymity::get_result(MAT data, int k) {

    if (k < 2 || k > data.size()) {
        throw invalid_argument("Error: The argument 'k' can't be smaller than 2 or larger than the number of records in this file!");
    }
    if (k != (int)k) {
        throw invalid_argument("Error: The argument 'k' should be an integer!");
    }

    //step 1: init the QID information of data
    QID.data2qid(data);

    //step 2: init the kd-tree root node
    vector<int> low(QID.get_len(), 0), high;
    MAT::iterator iter;
    vector<int> lis;
    for (iter = QID.val_list.begin(); iter != QID.val_list.end(); iter++) {
        lis = *iter;
        high.push_back(lis.size()-1);
    }
    KDTree kd_tree = KDTree(data, low, high, QID.get_len());

    //step 3: build the kd-tree partition on data
    DIVIDE.clear();
    my_partition(kd_tree, k);

    //step 4: get anonymized result by array 'DIVIDE'(each element is a 'KDTree' node)
    vector<KDTree>::iterator iter2;
    KDTree node;
    MAT records;
    RES result;
    vector<string> record;
    for (iter2=DIVIDE.begin(); iter2!=DIVIDE.end(); iter2++) {   // for each kd-tree node
        node = *iter2;
        records = node.data;
//        printf("%d\n", records.size());
        for (iter=records.begin(); iter!=records.end(); iter++) {
            record.clear();
            for (int index = 0; index < QID.get_len(); index++) {
                record.push_back(
                    merge_result(QID.val_list[index][node.low[index]],
                                 QID.val_list[index][node.high[index]])
                );
            }
            result.push_back(record);
        }
    }
    return result;
}


void k_anonymity(string infile, int QID_NUM, vector<int> QID_INDEX, int k, string outfile) {
    Reader r;
    K_Anonymity obj;
    try {
        r.read_k_anonymity(infile, QID_NUM, QID_INDEX);
        RES res_data = obj.get_result(r.data, k);
        RES result = r.convert_to_rawdata(res_data, r.is_str, r.inv_dict);
        r.write_to_file(result, outfile);
        printf("\n- Success!\n- The anonymous data has been written to %s file!\n\n",
               outfile.c_str());
    } catch (exception &e) {
        cerr << e.what() << endl;
    }
}


// -+-+-+-+-+-+-+-+-+-+-+<l_diversity.cpp>-+-+-+-+-+-+-+-+-+-+-+-+-+-+-


int L_Diversity::find_split_dimension(KDTree kd_tree) {
    int max_dim = -1;
    double max_dis = -1;
    for (int dim = 0; dim < FIELD.get_len(); dim++) {
        if (!kd_tree.flag[dim]) {
            continue;
        }
        vector<int> dim_list = FIELD.qid_list[dim];
        int value_range = attr_value(dim_list[kd_tree.high[dim]]) -
                          attr_value(dim_list[kd_tree.low[dim]]);
        int total_range = dim_list[dim_list.size()-1] - dim_list[0];
        double dis = (double)value_range / total_range;
        if (dis > max_dis) {
            max_dis = dis;
            max_dim = dim;
        }
    }
    return max_dim;
}


Tetrad L_Diversity::find_split_value(KDTree kd_tree, int dim) {
    // count number of each different value in each dimension
    map<int, int> value_count;          // (value -> cnt) dictionary for kd_tree.data[:, dim]
    vector<int> value_list;             // (value) list [unique/ascend] for kd_tree.data[:, dim]
    MAT::iterator iter;
    vector<int> record;
    map<int, int>::iterator iter_find;
    for (iter=kd_tree.data.begin(); iter!=kd_tree.data.end(); iter++) {
        record = *iter;
        iter_find = value_count.find(record[dim]);
        if (iter_find != value_count.end()) {
            value_count[record[dim]] += 1;
        } else {
            value_count[record[dim]] = 1;
            value_list.push_back(record[dim]);
        }
    }
    // get unique & ordered value in the given dimension of data
    sort(value_list.begin(), value_list.end());

    // special case: there is only one different value
    if (value_list.size() <= 1) {
        if (value_list.size() > 0) {
            return Tetrad(-INF, -INF, value_list[0], value_list.back());
        }
        return Tetrad(-INF, -INF, -INF, -INF);
    }

    // find the split value & index (median)
    int mid_count = kd_tree.data.size() / 2;
    int cnt = 0, split_index = 0, value, split_value, next_value;
    for (int i = 0; i < value_list.size(); i++) {
        value = value_list[i];
        cnt += value_count[value];
        if (cnt >= mid_count) {
            split_value = value;
            split_index = i;
            break;
        }
    }
    // get the value behind the split_val
    if (split_index + 1 < value_list.size()) {
        next_value = value_list[split_index + 1];
    } else {
        next_value = split_value;
    }
    return Tetrad(split_value, next_value, value_list[0], value_list.back());
}


bool L_Diversity::check_l_diversity(KDTree kd_tree, int l) {
    // case 1: total number of records is less than 'l'
    if (kd_tree.get_len() < l) {
        return false;
    }

    // case 2: total types of SA value is less than 'l'
    MAT records_set = kd_tree.data;
    int num_records = records_set.size();
    map<int, int> sa_dict;
    MAT::iterator iter;
    vector<int> record;
    int sa_value;
    map<int, int>::iterator iter2;
    for (iter=records_set.begin(); iter!=records_set.end(); iter++) {
        record = *iter;
        sa_value = record.back();
        iter2 = sa_dict.find(sa_value);
        if (iter2 != sa_dict.end()) {
            sa_dict[sa_value] += 1;
        } else {
            sa_dict[sa_value] = 1;
        }
    }
    if (sa_dict.size() < 1) {
        return false;
    }

    // case 3: if any SA value appear more than |T|/l
    for (iter2=sa_dict.begin(); iter2!=sa_dict.end(); iter2++) {
        if (sa_dict[iter2->first] > 1.0 * num_records / l) {
            return false;
        }
    }
    return true;
}


void L_Diversity::my_partition(KDTree kd_tree, int l) {
    // terminal condition: can not split anymore..
    if (!has_true_flag(kd_tree.flag)) {
        DIVIDE.push_back(kd_tree);
        return;
    }

    // choose split attribute
    int dim = find_split_dimension(kd_tree);
    // special case: can not choose any dimension
    if (dim == -1) {
        DIVIDE.push_back(kd_tree);
        return;
    }

    // choose split value
    Tetrad te = find_split_value(kd_tree, dim);
    int split_value = te.split_value, next_value = te.next_value;
    int low = te.low, high = te.high;
    // update low and high bound of this node
    if (low != -INF) {
        kd_tree.low[dim] = FIELD.qid_dict[dim][low];
        kd_tree.high[dim] = FIELD.qid_dict[dim][high];
    }
    // special case: cannot split -> try to find next best dimension
    if (split_value == -INF) {
        kd_tree.flag[dim] = false;
        my_partition(kd_tree, l);
        return;
    }

    // build the left-child & right-child
    int split_index = FIELD.qid_dict[dim][split_value];
    vector<int> lnode_high = kd_tree.high;
    lnode_high[dim] = split_index;
    vector<int> rnode_low = kd_tree.low;
    rnode_low[dim] = FIELD.qid_dict[dim][next_value];
    MAT sub_data;
    sub_data.clear();
    KDTree lnode = KDTree(sub_data, kd_tree.low, lnode_high, FIELD.get_len());
    KDTree rnode = KDTree(sub_data, rnode_low, kd_tree.high, FIELD.get_len());
    // judge the data in this node belong to left-child or right-child
    MAT mid_set;
    vector<int> record;
    MAT::iterator iter;
    for (iter=kd_tree.data.begin(); iter!=kd_tree.data.end(); iter++) {
        record = *iter;
        int idx = FIELD.qid_dict[dim][record[dim]];
        if (idx < split_index) {
            lnode.add_record(record);
        } else if (idx > split_index) {
            rnode.add_record(record);
        } else {
            mid_set.push_back(record);
        }
    }
    // attention: handle records which equal to record[split_index]
    int half_len = kd_tree.get_len() / 2;
    for (int i = 0; i < (half_len-lnode.get_len()); i++) {
        record = mid_set.back();
        mid_set.pop_back();
        lnode.add_record(record);
    }
    if (mid_set.size() > 0) {                    // there are extra multiple records..
        rnode.low[dim] = split_index;
        rnode.add_records(mid_set);
    }

    // anonymize sub-partition
    // try to split this node only when lnode & rnode satisfy conditions
    if (!check_l_diversity(lnode, l) || !check_l_diversity(rnode, l)) {
        DIVIDE.push_back(kd_tree);
        return;
    }
    my_partition(lnode, l);
    my_partition(rnode, l);
}


RES L_Diversity::get_result(MAT data, int l) {

    if (l < 1 || l > data.size()) {
        throw invalid_argument("Error: The argument 'l' can't be smaller than 1 or larger than the number of records in this file!");
    }
    if (l != (int)l) {
        throw invalid_argument("Error: The argument 'l' should be an integer!");
    }

    //step 1: init the FIELD information of data
    FIELD.data2qid(data);

    //step 2: init the kd-tree root node
    vector<int> low(FIELD.get_len(), 0), high;
    MAT::iterator iter;
    vector<int> lis;
    for (iter = FIELD.qid_list.begin(); iter != FIELD.qid_list.end(); iter++) {
        lis = *iter;
        high.push_back(lis.size()-1);
    }
    KDTree kd_tree = KDTree(data, low, high, FIELD.get_len());

    //step 3: build the kd-tree partition on data
    DIVIDE.clear();
    my_partition(kd_tree, l);

    //step 4: get anonymized result by array 'DIVIDE'(each element is a 'KDTree' node)
    vector<KDTree>::iterator iter2;
    KDTree node;
    MAT records;
    RES result;
    vector<string> record;
    for (iter2=DIVIDE.begin(); iter2!=DIVIDE.end(); iter2++) {   // for each kd-tree node
        node = *iter2;
        records = node.data;
        for (iter=records.begin(); iter!=records.end(); iter++) {
            record.clear();
            for (int index = 0; index < FIELD.get_len(); index++) {
                record.push_back(
                    merge_result(FIELD.qid_list[index][node.low[index]],
                                 FIELD.qid_list[index][node.high[index]])
                );
            }
            result.push_back(record);
        }
    }
    return result;
}


void l_diversity(string infile, int QID_NUM, vector<int> QID_INDEX,
                 int SA_INDEX, int l, string outfile) {
    Reader r;
    L_Diversity obj;
    try {
        r.read_l_diversity(infile, QID_NUM, QID_INDEX, SA_INDEX);
        RES res_data = obj.get_result(r.data, l);
        RES result = r.convert_to_rawdata(res_data, r.is_str, r.inv_dict);
        r.write_to_file(result, outfile);
        printf("\n- Success!\n- The anonymous data has been written to %s file!\n\n",
               outfile.c_str());
    } catch (exception &e) {
        cerr << e.what() << endl;
    }
}


// -+-+-+-+-+-+-+-+-+-+-+<t_closeness.h>-+-+-+-+-+-+-+-+-+-+-+-+-+-+-


int T_Closeness::find_split_dimension(KDTree kd_tree) {
    int max_dim = -1;
    double max_dis = -1;
    for (int dim = 0; dim < FIELD.get_len(); dim++) {
        if (!kd_tree.flag[dim]) {
            continue;
        }
        vector<int> dim_list = FIELD.qid_list[dim];
        double value_range = attr_value(dim_list[kd_tree.high[dim]]) -
                             attr_value(dim_list[kd_tree.low[dim]]);
        int total_range = dim_list[dim_list.size()-1] - dim_list[0];
        double dis = (double)value_range / total_range;
        if (dis > max_dis) {
            max_dis = dis;
            max_dim = dim;
        }
    }
    return max_dim;
}


Tetrad T_Closeness::find_split_value(KDTree kd_tree, int dim) {
    // count number of each different value in each dimension
    map<int, int> value_count;          // (value -> cnt) dictionary for kd_tree.data[:, dim]
    vector<int> value_list;             // (value) list [unique/ascend] for kd_tree.data[:, dim]
    MAT::iterator iter;
    vector<int> record;
    map<int, int>::iterator iter_find;
    for (iter=kd_tree.data.begin(); iter!=kd_tree.data.end(); iter++) {
        record = *iter;
        iter_find = value_count.find(record[dim]);
        if (iter_find != value_count.end()) {
            value_count[record[dim]] += 1;
        } else {
            value_count[record[dim]] = 1;
            value_list.push_back(record[dim]);
        }
    }
    // get unique & ordered value in the given dimension of data
    sort(value_list.begin(), value_list.end());

    // special case: there is only one different value
    if (value_list.size() <= 1) {
        if (value_list.size() > 0) {
            return Tetrad(-INF, -INF, value_list[0], value_list.back());
        }
        return Tetrad(-INF, -INF, -INF, -INF);
    }

    // find the split value & index (median)
    int mid_count = kd_tree.data.size() / 2;
    int cnt = 0, split_index = 0, value, split_value, next_value;
    for (int i = 0; i < value_list.size(); i++) {
        value = value_list[i];
        cnt += value_count[value];
        if (cnt >= mid_count) {
            split_value = value;
            split_index = i;
            break;
        }
    }
    // get the value behind the split_val
    if (split_index + 1 < value_list.size()) {
        next_value = value_list[split_index + 1];
    } else {
        next_value = split_value;
    }
    return Tetrad(split_value, next_value, value_list[0], value_list.back());
}


bool T_Closeness::check_t_closeness(KDTree kd_tree, double t) {
    // 1: get the distribution of SA value in this kd_tree node
    MAT records_set = kd_tree.data;
    int num_records = records_set.size();
    map<int, int> sa_dict;
    MAT::iterator iter;
    vector<int> record;
    int sa_value;
    map<int, int>::iterator iter2;
    for (iter=records_set.begin(); iter!=records_set.end(); iter++) {
        record = *iter;
        sa_value = record.back();
        iter2 = sa_dict.find(sa_value);
        if (iter2 != sa_dict.end()) {
            sa_dict[sa_value] += 1;
        } else {
            sa_dict[sa_value] = 1;
        }
    }
    map<int, double> sa_distribution;
    double sum_value = 0.0;
    for (iter2=sa_dict.begin(); iter2!=sa_dict.end(); iter2++) {
        sum_value += iter2->second;
    }
    for (iter2=sa_dict.begin(); iter2!=sa_dict.end(); iter2++) {
        int key = iter2->first;
        sa_distribution[key] = sa_dict[key] / sum_value;
    }

    // 2: get the distance between sa distribution on this node and that on the whole table
    double dis = 0.0;
    map<int, double>::iterator iter3, iter4;
    for (iter3=FIELD.sa_distribution.begin(); iter3!=FIELD.sa_distribution.end(); iter3++) {
        int key = iter3->first;
        double value = iter3->second;
        iter4 = sa_distribution.find(key);
        if (iter4 != sa_distribution.end()) {
            dis += 0.5 * abs(value - sa_distribution[key]);
        } else {
            dis += 0.5 * value;
        }
    }
    if (dis > t) {
        return false;
    }
    return true;
}


void T_Closeness::my_partition(KDTree kd_tree, double t) {
    // terminal condition: can not split anymore..
    if (!has_true_flag(kd_tree.flag)) {
        DIVIDE.push_back(kd_tree);
        return;
    }

    // choose split attribute
    int dim = find_split_dimension(kd_tree);
    // special case: can not choose any dimension
    if (dim == -1) {
        DIVIDE.push_back(kd_tree);
        return;
    }

    // choose split value
    Tetrad te = find_split_value(kd_tree, dim);
    int split_value = te.split_value, next_value = te.next_value;
    int low = te.low, high = te.high;
    // update low and high bound of this node
    if (low != -INF) {
        kd_tree.low[dim] = FIELD.qid_dict[dim][low];
        kd_tree.high[dim] = FIELD.qid_dict[dim][high];
    }
    // special case: cannot split -> try to find next best dimension
    if (split_value == -INF) {
        kd_tree.flag[dim] = false;
        my_partition(kd_tree, t);
        return;
    }

    // build the left-child & right-child
    int split_index = FIELD.qid_dict[dim][split_value];
    vector<int> lnode_high = kd_tree.high;
    lnode_high[dim] = split_index;
    vector<int> rnode_low = kd_tree.low;
    rnode_low[dim] = FIELD.qid_dict[dim][next_value];
    MAT sub_data;
    sub_data.clear();
    KDTree lnode = KDTree(sub_data, kd_tree.low, lnode_high, FIELD.get_len());
    KDTree rnode = KDTree(sub_data, rnode_low, kd_tree.high, FIELD.get_len());
    // judge the data in this node belong to left-child or right-child
    MAT mid_set;
    vector<int> record;
    MAT::iterator iter;
    for (iter=kd_tree.data.begin(); iter!=kd_tree.data.end(); iter++) {
        record = *iter;
        int idx = FIELD.qid_dict[dim][record[dim]];
        if (idx < split_index) {
            lnode.add_record(record);
        } else if (idx > split_index) {
            rnode.add_record(record);
        } else {
            mid_set.push_back(record);
        }
    }
    // attention: handle records which equal to record[split_index]
    int half_len = kd_tree.get_len() / 2;
    for (int i = 0; i < (half_len-lnode.get_len()); i++) {
        record = mid_set.back();
        mid_set.pop_back();
        lnode.add_record(record);
    }
    if (mid_set.size() > 0) {                    // there are extra multiple records..
        rnode.low[dim] = split_index;
        rnode.add_records(mid_set);
    }

    // anonymize sub-partition
    // try to split this node only when lnode & rnode satisfy conditions
    if (!check_t_closeness(lnode, t) || !check_t_closeness(rnode, t)) {
        DIVIDE.push_back(kd_tree);
        return;
    }
    my_partition(lnode, t);
    my_partition(rnode, t);
}


RES T_Closeness::get_result(MAT data, double t) {

    if (t < 0) {
        throw invalid_argument("Error: The argument 't' can't be smaller than 0!");
    }

    //step 1: init the FIELD information of data
    FIELD.data2qid(data);

    //step 2: init the kd-tree root node
    vector<int> low(FIELD.get_len(), 0), high;
    MAT::iterator iter;
    vector<int> lis;
    for (iter = FIELD.qid_list.begin(); iter != FIELD.qid_list.end(); iter++) {
        lis = *iter;
        high.push_back(lis.size()-1);
    }
    KDTree kd_tree = KDTree(data, low, high, FIELD.get_len());

    //step 3: build the kd-tree partition on data
    DIVIDE.clear();
    my_partition(kd_tree, t);

    //step 4: get anonymized result by array 'DIVIDE'(each element is a 'KDTree' node)
    vector<KDTree>::iterator iter2;
    KDTree node;
    MAT records;
    RES result;
    vector<string> record;
    for (iter2=DIVIDE.begin(); iter2!=DIVIDE.end(); iter2++) {   // for each kd-tree node
        node = *iter2;
        records = node.data;
        for (iter=records.begin(); iter!=records.end(); iter++) {
            record.clear();
            for (int index = 0; index < FIELD.get_len(); index++) {
                record.push_back(
                    merge_result(FIELD.qid_list[index][node.low[index]],
                                 FIELD.qid_list[index][node.high[index]])
                );
            }
            result.push_back(record);
        }
    }
    return result;
}


void t_closeness(string infile, int QID_NUM, vector<int> QID_INDEX,
                 int SA_INDEX, double t, string outfile) {
    Reader r;
    T_Closeness obj;
    try {
        r.read_t_closeness(infile, QID_NUM, QID_INDEX, SA_INDEX);
        RES res_data = obj.get_result(r.data, t);
        RES result = r.convert_to_rawdata(res_data, r.is_str, r.inv_dict);
        r.write_to_file(result, outfile);
        printf("\n- Success!\n- The anonymous data has been written to %s file!\n\n",
               outfile.c_str());
    } catch (exception &e) {
        cerr << e.what() << endl;
    }
}


