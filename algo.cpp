#include <vector>
#include <iostream>
using std::vector;
void dfs(vector<int>& value, vector<int>& cur_res, int num ,int limitValue, int cur_index, int& result){
	if(cur_index == num){
        int sum =0;
        for(int i = 0 ; i <cur_res.size();i++)
            sum += cur_res[i];
        result = std::max(result , sum);
    }
    cur_res.push_back(value[cur_index]);
    dfs(value,cur_res,num,limitValue,cur_index + 1,result);
    cur_res.pop_back();
    dfs(value,cur_res,num,limitValue,cur_index + 1,result);
}

int main(){
    vector<int> value(10,0);
    std::cout<<value.size();
    
    for(int i = 0 ;i < value.size() ; i++){
        value[i] = i;
    }
    std::cout<<"here";
    int result = 0;
    vector<int> cur_res;
    dfs(value, cur_res, value.size(), 10 , 0 , result);
    std::cout<<result;
    return 0;

}