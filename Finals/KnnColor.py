from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np
from pprint import pprint

class KnnClassifier:
    def __init__(self,n):
        self.colorData = {
            'data': ([[179, 117, 0] ,[119, 51, 0] ,[120, 42, 6] ,[254, 253, 65] ,[143, 48, 0] ,[255, 0, 0] ,[255, 127, 0] ,[87, 59, 15] ,[221, 193, 26] ,[151, 4, 1] ,[187, 90, 2] ,[219, 173, 132] ,[233, 191, 12] ,[106, 56, 1] ,[53, 0, 2] ,[252, 101, 1] ,[210, 169, 109] ,[255, 0, 0] ,[210, 116, 25] ,[142, 115, 79] ,[186, 72, 0] ,[168, 130, 34] ,[237, 160, 36] ,[179, 119, 0] ,[193, 119, 1] ,[ 161 , 147 , 70 ],[ 145 , 134 , 60 ],[ 184 , 170 , 86 ],[ 172 , 157 , 78 ],[ 193 , 180 , 105 ],[ 131 , 121 , 53 ],[ 133 , 122 , 54 ],[ 148 , 138 , 73 ],[ 143 , 133 , 69 ],
                    [53, 82, 32] ,[3, 130, 86] ,[140, 217, 159] ,[13, 141, 60] ,[74, 87, 17] ,[0, 53, 3] ,[131, 181, 118] ,[0, 100, 0] ,[53, 82, 32] ,[0, 254, 0] ,[17, 67, 35] ,[100, 184, 51] ,[1, 128, 0] ,[0, 100, 0] ,[1, 128, 0] ,[60, 107, 0] ,[0, 255, 102] ,[104, 172, 84] ,[81, 166, 0] ,[88, 232, 125] ,[170, 205, 102] ,[85, 189, 64] ,[38, 202, 37] ,[1, 252, 123] ,[75, 194, 125] ,[ 25 , 178 , 129 ],[ 32 , 212 , 154 ],[ 33 , 214 , 156 ],[ 22 , 145 , 103 ],[ 26 , 181 , 132 ],[ 36 , 231 , 171 ],[ 32 , 195 , 144 ],[ 29 , 195 , 142 ],[ 29 , 185 , 135 ],
                    [0, 103, 254] ,[0, 127, 254] ,[33, 87, 255] ,[0, 102, 255] ,[1, 122, 255] ,[24, 117, 255] ,[0, 127, 255] ,[0, 103, 255] ,[0, 153, 255] ,[3, 53, 255] ,[0, 103, 255] ,[3, 53, 255] ,[0, 160, 255] ,[19, 79, 252] ,[59, 111, 253] ,[36, 113, 255] ,[0, 165, 255] ,[33, 100, 253] ,[52, 112, 255] ,[0, 103, 254] ,[0, 102, 254] ,[0, 127, 255] ,[40, 141, 255] ,[0, 95, 255] ,[35, 97, 235] ,[ 9 , 71 , 181 ],[ 10 , 58 , 154 ],[ 11 , 84 , 196 ],[ 12 , 78 , 184 ],[ 11 , 88 , 207 ],[ 13 , 101 , 224 ],[ 12 , 90 , 209 ],[ 17 , 137 , 243 ],[ 15 , 116 , 242 ],[ 10 , 61 , 170 ],
                    [1, 0, 119] ,[2, 0, 254] ,[67, 4, 157] ,[0, 17, 148] ,[24, 5, 205] ,[75, 5, 176] ,[3, 3, 67] ,[32, 16, 207] ,[53, 15, 253] ,[0, 0, 132] ,[0, 0, 139] ,[13, 0, 255] ,[0, 0, 132] ,[0, 0, 253] ,[32, 0, 144] ,[0, 21, 204] ,[23, 23, 128] ,[0, 17, 148] ,[19, 1, 115] ,[3, 13, 61] ,[25, 30, 172] ,[31, 28, 208] ,[23, 23, 209] ,[5, 0, 182] ,[32, 16, 207] ,[ 141 , 103 , 193 ],[ 116 , 82 , 164 ],[ 158 , 120 , 212 ],[ 118 , 82 , 163 ],[ 132 , 96 , 180 ],[ 128 , 91 , 177 ],[ 156 , 119 , 211 ],[ 146 , 111 , 199 ],
                    [235, 230, 225] ,[251, 251, 252] ,[231, 237, 255] ,[210, 215, 214] ,[244, 249, 251] ,[223, 220, 219] ,[201, 198, 192] ,[228, 233, 242] ,[209, 202, 201] ,[236, 236, 236] ,[208, 204, 205] ,[228, 233, 242] ,[221, 224, 229] ,[222, 230, 239] ,[205, 209, 210] ,[193, 189, 191] ,[192, 192, 192] ,[254, 249, 248] ,[227, 239, 243] ,[204, 192, 188] ,[228, 241, 251] ,[198, 197, 198] ,[195, 200, 191] ,[199, 198, 197] ,[224, 223, 217] ,[ 155 , 185 , 162 ],[ 138 , 164 , 144 ],[ 179 , 209 , 184 ],[ 163 , 192 , 168 ],[ 128 , 153 , 137 ],[ 129 , 154 , 137 ],[ 144 , 173 , 151 ],[ 216 , 243 , 218 ],[ 214 , 242 , 217 ],
                    [17, 255, 255] ,[4, 234, 251] ,[39, 242, 254] ,[49, 255, 255] ,[9, 183, 255] ,[127, 255, 254] ,[39, 191, 246] ,[94, 217, 249] ,[0, 166, 255] ,[20, 255, 255] ,[11, 213, 253] ,[22, 209, 252] ,[1, 253, 255] ,[79, 255, 223] ,[2, 227, 255] ,[51, 255, 255] ,[10, 182, 213] ,[92, 220, 253] ,[93, 252, 252] ,[23, 224, 247] ,[121, 252, 255] ,[64, 254, 255] ,[122, 254, 255] ,[0, 241, 253] ,[0, 255, 255], [ 19 , 184 , 197 ],[ 9 , 157 , 170 ],[ 15 , 177 , 191 ],[ 23 , 201 , 215 ],[ 27 , 211 , 224 ],[ 15 , 178 , 192 ],[ 22 , 186 , 197 ],[ 15 , 172 , 185 ]
                    ]),
            'target':[0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0,0,0,0,0,0,0,0,0,
                    1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1,1,1,1,1,1,1,1,1,
                    2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2,2,2,2,2,2,2,2,2,2,
                    3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,3,3,3,3,3,3,3,3,3 ,
                    4 ,4 ,4 ,4 ,4 ,4 ,4 ,4 ,4 ,4 ,4 ,4 ,4 ,4 ,4 ,4 ,4 ,4 ,4 ,4 ,4 ,4 ,4 ,4 ,4 ,4,4,4,4,4,4,4,4,4,
                    5 ,5 ,5 ,5 ,5 ,5 ,5 ,5 ,5 ,5 ,5 ,5 ,5 ,5 ,5 ,5 ,5 ,5 ,5 ,5 ,5 ,5 ,5 ,5 ,5,5,5,5,5,5,5,5,5],
            'target_name':['blue','green','orange','red','white','yellow']
        }
        xtrain, xtest, ytrain, ytest = train_test_split(self.colorData['data'], self.colorData['target'], test_size = 0.1, random_state = 4)
        self.classifier = KNeighborsClassifier(n_neighbors=n)
        self.classifier.fit(xtrain, ytrain)
    
    def CreateKNN(self):
        xtrain, xtest, ytrain, ytest = train_test_split(self.colorData['data'], self.colorData['target'], test_size = 0.1, random_state = 4)
        #------ Feature Scaling
        scaler = StandardScaler()
        scaler.fit(xtrain)
        xtrain = scaler.transform(xtrain)
        xtest = scaler.transform(xtest)
        #-----------------------------------
        classifier = KNeighborsClassifier(n_neighbors=7)
        classifier.fit(xtrain, ytrain)

    def PredictColor(self,r,g,b):
        y_pred = self.classifier.predict([[r, g, b]])
        return self.colorData['target_name'][y_pred[0]]
