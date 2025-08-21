#include<iostream>
#include<vector>
#include<algorithm>
#include<fstream>
using namespace std;
int main(int argc,char* argv[]){
	if(argc<3){
		return 0;
	}
	int row=atoi(argv[1]),col=atoi(argv[2]),i,j,k=3,l,medium;
	ifstream fp;
	fp.open(argv[3]);
	vector <int> v;
	vector < vector <int> > arr(row,vector<int>(col,0));
	for(i=0;i<row;i++){
		for(j=0;j<col;j++){
			fp>>arr[i][j];
		}
	}
	for (i = 0; i < row; i++) {
		for (j = 0; j < col; j++) {
			if (i == 0 || i == row - 1 || j == 0 || j == col - 1) {
				cout << arr[i][j] << " ";
			} else {
				v.clear();
				for (k = -1; k <= 1; k++) {
					for (l = -1; l <= 1; l++) {
						v.push_back(arr[i + k][j + l]);
					}
				}
				sort(v.begin(), v.end());
				cout << v[v.size() / 2] << " ";
			}
		}
		cout << endl;
	}
	return 2;
}
