import numpy as np
import os

class FileOperation:
    @staticmethod
    def ReadFile(file_name:str)->dict:
        default_root='env'
        list=[]
        path=os.path.join(default_root,file_name)
        with open(path, 'r') as f:
            for line in f:
                line = line.strip('\n').strip()
                list.append(line)
        f.close()
        envrionemt=[]
        size=[]
        row_number=[]
        column_number=[]
        for i in range(len(list)):
            if i==0:
                temp=list[i].split(' ')
                for item in temp:
                    size.append(int(item))
            elif i== len(list)-1:
                temp=list[i].split()
                for item in temp:
                    column_number.append(int(item))
            else:
                env=[]
                temp=list[i].replace(' ','')
                for j in range(len(temp)):
                    if j==len(temp)-1:
                        row_number.append(int(temp[j]))
                    else:
                        env.append(temp[j])
                envrionemt.append(env)
        new_environment=np.zeros((size[0],size[1]))
        for i in range(len(envrionemt)):
            line=[]
            for j in range(len(envrionemt[0])):
                if envrionemt[i][j]=='.':
                    new_environment[i,j]=int(0)
                elif envrionemt[i][j]=='T':
                    new_environment[i,j]=int(-1)
        result={}
        #the structure of result is like ['environment','size','row_number','colum_number']
        result['environment']=np.array(new_environment)
        result['size']=np.array(size)
        result['row_number']=np.array(row_number)
        result['column_number']=np.array(column_number)
        return result
    @staticmethod
    def PrintDict(input:dict):
        keys=input.keys()
        for item in keys:
            print(item)
            print(input[item])
    @staticmethod
    def GetFileNameList(path='env'):
        for root, dirs, files in os.walk(path):
            return files

if __name__ == '__main__':
    file="tents-25x30-t.txt"
    result=FileOperation.ReadFile(file)
    print(result['environment'])
    print(result['size'])
    print(result['row_number'])
    print(result['column_number'])
    FileOperation.PrintDict(result)


