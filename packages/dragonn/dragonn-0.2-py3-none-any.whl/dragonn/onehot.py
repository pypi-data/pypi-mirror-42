from numpy import array
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

label_encoder = LabelEncoder()
onehot_encoder = OneHotEncoder(sparse=False)

sequences=["ACGTACGTACGT","TGCATGCATGCA"]
int_seq=[]
for s in sequences:
    int_seq.append(label_encoder.fit_transform(list(s)))
    
#reshape because that's what OneHotEncoder likes
#integer_encoded_seq = integer_encoded_seq.reshape(len(integer_encoded_seq), 1)
#onehot_encoded_seq = onehot_encoder.fit_transform(integer_encoded_seq)
onehot_encoded_seq = onehot_encoder.fit_transform(int_seq)
print(onehot_encoded_seq.shape)
print(onehot_encoded_seq)
