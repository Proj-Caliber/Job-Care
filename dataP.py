class DHL:
    '''
    # co-author : @qkrwjdduf159, @AshbeeKim, @oliviachchoi
    # contributor : @kim-hyun-ho
    # co-author could be changed depands on our Team's decision
    모델은 현재 점수가 가장 높게 나왔던 정열님 모델을 기본 구조로 작성할 예정
    따라서 데이터 초반 flow는 기본 형태에서 크게 벗어나지 않는 선에서 맞출 필요 있음
    class 내 property는 def별 활용이 높거나, 기본 변수를 해하지 않도록 선언
    train, test의 경우, 기본 제공 데이터에서 EDA 중 변수가 늘어날 수 있기에 함수 내 불러올 데이터만 조정하면 되도록 작성
    '''
    code_list = []
    for csv in glob("./*.csv"):
        if re.sub("[ㄱ-힣]", "", csv)[2]=="_":
            code_list.append(csv)
    for csv in code_list:
        _n = (re.sub("[^a-zA-Z]", "", csv.split(".")[1])).lower()
        locals()[f"{_n}_df"] = pd.read_csv(csv, encoding="utf-8", index_col=0).T.to_dict()

    train = eval("train_DF")
    test = eval("test_DF")
    
    def __init__(self):
        self.train, self.match_cols = self.convert_code("train")
        self.test = self.convert_code("test")

    def _from_cols(self):
        '''
        d/h/l 코드 데이터에서 불러와야 할 코드값과 반복될 경우의 수
        '''
        _func = lambda x: x.split(' ')
        cols_info, lenC = [], []

        for c_type in ["d", "h", "l"]:
            comp = eval(f"self.{c_type}_df")
            cols = [col for col in list(comp[list(comp.keys())[0]].keys())]
            lenC.extend([len(cols) for cnt in range(len(cols))])
            cols_info.extend(cols)
        return cols_info, lenC
    
    def _add_drop_cols(self):
        '''
        추후 진행할 EDA 혹은 FE 중 대중소세의 분류 관계가 제대로 매핑되지 않았을 경우, _cat을 수정
        "l" 코드 관련 내용은 "contents_attribute"만 추가되도록 예외 처리
        반복될 경우의 수를 기반으로 대중소세값 관련 항목 추가
        '''
        add_cols, drop_cols, repeat_cols = [], [], []

        _cat = {"대": "l", "중": "m", "소": "s", "세": "n"}
        _case = {"p": "person_prefer", "c": "contents_attribute"}
        _fcols, _num = self._from_cols()

        for num, col in zip(_num, _fcols):
            _val = _cat.get((col.split(" "))[-1][0])
            _t = (re.sub("[^a-zA-Z]", "", col)).lower()
            if _t != "l":
                for idx in range(1, num):
                    add_cols.append("_".join([_case["p"], _t, str(idx), _val]))
                    drop_cols.append("_".join([_case["p"], _t, str(idx)]))
                    repeat_cols.append(col)
                add_cols.append("_".join([_case["c"], _t, _val]))
                drop_cols.append("_".join([_case["c"], _t]))
                repeat_cols.append(col)
            else:
                add_cols.append("_".join([_case["c"], _t, _val]))
                drop_cols.append("_".join([_case["c"], _t]))
                repeat_cols.append(col)

        return add_cols, drop_cols, repeat_cols

    def convert_code(self, datas):
        '''
        반환된 추가 항목, 제거 항목, 반복 항목명을 기준으로 데이터 처리
        '''
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
        '''
        반환된 추가 항목과 train 데이터의 평균값을 기준으로 train, test 데이터 처리
        '''
        for col in self.match_cols:
            _gbm = self.train.groupby(col)['target'].mean()
            self.train[col] = self.train[col].map(dict(_gbm.items()))
            self.test[col] = self.test[col].map(dict(_gbm.items()))

    def control_params(self, *kwargs):
        '''
        최종 drop, dummpy 할 변수 반환
        반환하는 지역 변수가 self.train, self.test와 다르기 때문에 여러 차례 변수를 조율할 수 있음
        '''
        f_train = self.train if drop_column is None else self.train.drop(drop_column, axis=1)
        f_test = self.test if drop_column is None else self.test.drop(drop_column, axis=1)
        
        self.f_train = f_train if dummy_column is None else  pd.get_dummies(data = f_train, columns=dummy_column, drop_first=True)
        self.f_test = f_test if dummy_column is None else  pd.get_dummies(data = f_test, columns=dummy_column, drop_first=True)
