# KeyError를 처리하면, 해당 클래스로 현재 대회 데이터 바로 처리 가능할 것임

class DHL:
    '''
    # co-author : @qkrwjdduf159, @AshbeeKim
    # co-author could be changed depands on our Team's decision
    모델은 현재 점수가 가장 높게 나왔던 정열님 모델을 기본 구조로 작성할 예정
    따라서 데이터 초반 flow는 기본 형태에서 크게 벗어나지 않는 선에서 맞출 필요 있음
    class 내 property는 def별 활용이 높거나, 기본 변수를 해하지 않도록 선언
    train, test의 경우, 기본 제공 데이터에서 EDA 중 변수가 늘어날 수 있기에 함수 내 불러올 데이터만 조정하면 되도록 작성
    '''
    d_df = eval("D_DF").copy()
    h_df = eval("H_DF").copy()
    l_df = eval("L_DF").copy()
    train = eval("train_DF").copy()
    test = eval("test_DF").copy()
    
    def __init__(self):
        self.train, self.match_cols = self.convert_code("train")
        self.test = self.convert_code("test")

        print(f"\n{self.match_cols}\n\n{self.train.head(10)}\n\n{self.test.head(10)}")
        self.groupby_mean()

    def _from_cols(self):
        _func = lambda x: x.split(' ')
        cols_info, lenC = [], []
        for c_type in ["d", "h", "l"]:
            comp = eval(f"self.{c_type}_df")
            cols = list(map(lambda col: _func(col), comp.columns))
            cols = [col for col in cols if "코드" not in col]
            lenC.append(len(cols))
            cols_info.extend(cols)
            # len 필요함, 열에 따라 다르게 들어감.
        return cols_info, lenC
    
    def _add_drop_cols(self):
        add_cols, drop_cols, repeat_cols = [], [], []

        _cat = {"대": "l", "중": "m", "소": "s", "세": "n"}
        _case = {"p": "person_prefer", "c": "contents_attribute"}
        _fcols, _num = self._from_cols()
        print(_fcols)
        for num, _key in zip(_num, _fcols):
            print(num, _key)
            _col, _val = " ".join(_key), _cat.get(_key[-1][0])
            _t = (re.sub("[^a-zA-Z]", "", _col)).lower()
            print(_t)
            if _t != "l":
                for idx in range(1, num+1):
                    add_cols.append("_".join([_case["p"], _t, str(idx), _val]))
                    drop_cols.append("_".join([_case["p"], _t, str(idx)]))
                    repeat_cols.append(_col)
                add_cols.append("_".join([_case["c"], _t, _val]))
                drop_cols.append("_".join([_case["c"], _t]))
                repeat_cols.append(_col)
            else:
                add_cols.append("_".join([_case["c"], _t, _val]))
                drop_cols.append("_".join([_case["c"], _t]))
                repeat_cols.append(_col)

        return add_cols, drop_cols, repeat_cols

    def convert_code(self, datas):
        DF = eval(f"self.{datas}").copy()

        adds, drops, repeats = self._add_drop_cols()
        for _a, _d, _r in zip(adds, drops, repeats):
            _t = (re.sub("[^a-zA-Z]", "", _r)).lower()
            comp = eval(f"self.{_t}_df")
            DF[_a] = DF[_d].apply(lambda x: comp[x][_r])

        if datas == "train":
            return DF.drop(drops, axis=1), adds
        else:
            return DF.drop(drops, axis=1)

    def groupby_mean(self):
        self.train, self.add_cols = self.add_code("train")
        self.test = self.add_code("test")

        for col in self.add_cols:
            _gpm = self.groupby(col)['target'].mean()
            self.train[col] = self.train[col].map(_gmp.items())
            self.test[col] = self.test[col].map(_gmp.items())

    def control_params(self, *kwargs):
        '''
        최종 drop, dummpy 할 변수 반환
        반환하는 지역 변수가 self.train, self.test와 다르기 때문에 여러 차례 변수를 조율할 수 있음
        '''
        f_train = self.train if drop_column is None else self.train.drop(drop_column, axis=1)
        f_test = self.test if drop_column is None else self.test.drop(drop_column, axis=1)
        
        self.f_train = f_train if dummy_column is None else  pd.get_dummies(data = f_train, columns=dummy_column, drop_first=True)
        self.f_test = f_test if dummy_column is None else  pd.get_dummies(data = f_test, columns=dummy_column, drop_first=True)
