#include <iostream>
#include <vector>
#include <string>
#include <bitset>
#include <algorithm>

using namespace std;

//================ Hàm hỗ trợ =================//

string convert_decimal_to_binary(int decimal)
{
    return bitset<4>(decimal).to_string();
}

int convert_binary_to_decimal(const string& binary)
{
    return stoi(binary, nullptr, 2);
}

string Xor(const string& a, const string& b)
{
    string result = "";
    for (int i = 0; i < a.size(); i++)
    {
        if (a[i] == b[i])
            result += '0';
        else
            result += '1';
    }
    return result;
}

//================ Hoán vị ban đầu =================//

int initial_permutation_table[64] =
{
58,50,42,34,26,18,10,2,
60,52,44,36,28,20,12,4,
62,54,46,38,30,22,14,6,
64,56,48,40,32,24,16,8,
57,49,41,33,25,17,9,1,
59,51,43,35,27,19,11,3,
61,53,45,37,29,21,13,5,
63,55,47,39,31,23,15,7
};

string initial_permutation(string input)
{
    string permuted = "";

    for(int i=0;i<64;i++)
        permuted += input[initial_permutation_table[i]-1];

    return permuted;
}

//================ Hoán vị ngược =================//

int inverse_permutation[64]=
{
40,8,48,16,56,24,64,32,
39,7,47,15,55,23,63,31,
38,6,46,14,54,22,62,30,
37,5,45,13,53,21,61,29,
36,4,44,12,52,20,60,28,
35,3,43,11,51,19,59,27,
34,2,42,10,50,18,58,26,
33,1,41,9,49,17,57,25
};

string inverse_initial_permutation(string input)
{
    string permuted="";

    for(int i=0;i<64;i++)
        permuted+=input[inverse_permutation[i]-1];

    return permuted;
}

//================ Tạo khóa =================//

class KeyGenerator
{
private:

string key;
vector<string> roundKeys;

int pc1[56] =
{
57,49,41,33,25,17,9,
1,58,50,42,34,26,18,
10,2,59,51,43,35,27,
19,11,3,60,52,44,36,
63,55,47,39,31,23,15,
7,62,54,46,38,30,22,
14,6,61,53,45,37,29,
21,13,5,28,20,12,4
};

int pc2[48]=
{
14,17,11,24,1,5,
3,28,15,6,21,10,
23,19,12,4,26,8,
16,7,27,20,13,2,
41,52,31,37,47,55,
30,40,51,45,33,48,
44,49,39,56,34,53,
46,42,50,36,29,32
};

string shift_left(string k)
{
    return k.substr(1)+k[0];
}

public:

KeyGenerator(string key)
{
    this->key=key;
}

void generate()
{
    string permuted="";

    for(int i=0;i<56;i++)
        permuted+=key[pc1[i]-1];

    string left=permuted.substr(0,28);
    string right=permuted.substr(28,28);

    for(int i=0;i<16;i++)
    {
        left=shift_left(left);
        right=shift_left(right);

        string combined=left+right;

        string round="";
        for(int j=0;j<48;j++)
            round+=combined[pc2[j]-1];

        roundKeys.push_back(round);
    }
}

vector<string> getKeys()
{
    return roundKeys;
}

};

//================ DES =================//

class DES
{
private:

vector<string> keys;

public:

DES(vector<string> keys)
{
    this->keys=keys;
}

string encrypt(string plaintext)
{
    string perm=initial_permutation(plaintext);

    string left=perm.substr(0,32);
    string right=perm.substr(32,32);

    for(int i=0;i<16;i++)
    {
        string newRight=Xor(left,keys[i].substr(0,32));

        left=right;
        right=newRight;
    }

    string combined=right+left;

    return inverse_initial_permutation(combined);
}

string decrypt(string ciphertext)
{
    reverse(keys.begin(),keys.end());

    string result=encrypt(ciphertext);

    reverse(keys.begin(),keys.end());

    return result;
}

};

//================ Triple DES =================//

string triple_encrypt(
string text,
vector<string> k1,
vector<string> k2,
vector<string> k3)
{
DES des1(k1);
DES des2(k2);
DES des3(k3);

text=des1.encrypt(text);
text=des2.decrypt(text);
text=des3.encrypt(text);

return text;
}

string triple_decrypt(
string text,
vector<string> k1,
vector<string> k2,
vector<string> k3)
{
DES des1(k1);
DES des2(k2);
DES des3(k3);

text=des3.decrypt(text);
text=des2.encrypt(text);
text=des1.decrypt(text);

return text;
}

//================ MAIN =================//

int main()
{
string plaintext;
string key1,key2,key3;

cout<<"Nhap Plaintext 64 bit: ";
cin>>plaintext;

cout<<"Nhap Key1: ";
cin>>key1;

cout<<"Nhap Key2: ";
cin>>key2;

cout<<"Nhap Key3: ";
cin>>key3;

KeyGenerator k1(key1);
k1.generate();

KeyGenerator k2(key2);
k2.generate();

KeyGenerator k3(key3);
k3.generate();

string cipher=
triple_encrypt(
plaintext,
k1.getKeys(),
k2.getKeys(),
k3.getKeys()
);

cout<<"Ciphertext: "<<cipher<<endl;

string plain=
triple_decrypt(
cipher,
k1.getKeys(),
k2.getKeys(),
k3.getKeys()
);

cout<<"Giai ma: "<<plain<<endl;

return 0;
}