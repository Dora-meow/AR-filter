#include<iostream>
#include<vector>
#include<algorithm>
#include<string>
#include<cmath>
#include <iostream>
using namespace std;
int main(int argc, char* argv[]) {
    if (argc < 4){
    	return 1;
	}
	int row = atoi(argv[1]), col = atoi(argv[2]),split=atoi(argv[3]);
	ios::sync_with_stdio(false); // 禁用與 C 流的同步
	cin.tie(NULL);           // 解綁 cin 和 cout
	cout.tie(NULL);          // 解綁 cout
	vector<vector<int> > arr(row, vector<int>(col, 0)),ans(row, vector<int>(col, 0));
    int i,j,k;
    for (int i = 0; i < row; ++i)
        for (int j = 0; j < col; ++j)
            cin >> arr[i][j];
	for (j=0;j<col;j++){
		ans[0][j]=arr[0][j];
		ans[row-1][j]=arr[row-1][j];
	}
	for(i=0;i<row;i++){
		ans[i][0]=arr[i][0];
		ans[i][col-1]=arr[i][col-1];
	}
    for (i = 1; i < row - 1; ++i) {
        for ( j = 1; j < col - 1; ++j) {
            vector<int> v;
            for (k = -1; k <= 1; ++k)
                for (int l = -1; l <= 1; ++l)
                    v.push_back(arr[i + k][j + l]);
            sort(v.begin(), v.end());
            ans[i][j]=v[v.size() / 2]; 
        }
    }
    int diff;
    for(i=0;i<row-1;i++){
    	for(j=0;j<col-1;j++){
    		diff=ans[i][j+1]-ans[i][j];
    		for(k=0;k<=split-1;k++){
    			cout<<int(6*diff*pow((k/split),5)-15*diff*pow((k/split),4)+10*diff*pow((k/split),3)+ans[i][j]);
    			//cout<<int(-3/11*ans[i+1][j]*pow(k/3,5)+15/22*ans[i+1][j]*pow(k/3)+13/22(pow(k/3,3))+ans[i][j]);
    			 if (j < col - 2 || k!=split-1) cout << ",";
			}
		}
		cout<<endl;
		for(int l=0;l<split-1;l++){
			for(j=0;j<col-1;j++){
				diff=ans[i][j+1]-ans[i][j];
    			for(k=0;k<=split-1;k++){
    				cout<<int(6*diff*pow((k/split),5)-15*diff*pow((k/split),4)+10*diff*pow((k/split),3)+ans[i][j]);
    				//cout<<ans[i][j]*int(k/3)+ans[i+1][j]*int(1-k/3);
    			 	if (j < col - 2 || k!=split-1) cout << ",";
				}
			}
			cout<<endl;
		}
	}
    return 0;
}

