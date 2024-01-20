import pulp

vars = dict()
problem = pulp.LpProblem('Simple_Problem', pulp.LpMaximize)

#入力データファイルを読み込む
def read_input(path : str) -> dict[str, list]:
    ret : dict[str, list] = dict()
    with open(path, "r") as file:
        lines = file.readlines()
        for line in lines:
            values = line.strip().split(",")
            name, holidays = values[0], values[1:]
            ret[name] = holidays

    return ret

#結果を出力
def output(path : str, worker_dict : dict[str, list]) -> None :
    
    with open(path, "w") as file:
        for name, holiday_plans in worker_dict.items():
            file.write(f"{name},")
            for shift, holiday_plan in enumerate(holiday_plans):
                var = getWorkerVar(name, shift)
                if(var is None):
                    file.write(f",-1")
                else:
                    file.write(f",{pulp.value(var)}")
            file.write("\n")
    return 

#変数を取得する
def getWorkerVar(key1, key2) -> pulp.LpVariable:    
    return vars.get(f"{key1},{key2}", None)
def getWorkIdVar(key1, key2, key3) -> pulp.LpVariable:
    return vars.get(f"{key1},{key2},{key3}", None)

#変数を生成する
def create_variables(worker_dict : dict[str, list], n_worker : list) -> None:
    global problem

    for name, holiday_plans in worker_dict.items():
        for shift, holiday_plan in enumerate(holiday_plans):
            if(holiday_plan == "-1"):
                continue
            
            key = f"{name},{shift}"
            vars[key] = pulp.LpVariable(key, lowBound=0, upBound=1, cat = pulp.const.LpContinuous)            

            for i in range(n_worker[shift]):
                key = f"{name},{shift},{i}"
                vars[key] = pulp.LpVariable(key, lowBound=0, upBound=1, cat = pulp.const.LpContinuous)

    return 

#制約式を追加する
#制約①：1日もしくは1シフトの中の必要人数を確保する
#制約②：作業員は連続して勤務できない
def create_cons(worker_dict : dict[str, list], n_worker : list) -> None:
    global problem
    for shift, n in enumerate(n_worker):
        for i in range(n):            
            linExpr = [ getWorkIdVar(name, shift, i) for name in worker_dict.keys() ]
            linExpr = [ var for var in linExpr if var is not None ]            
            problem.addConstraint(constraint = sum(linExpr) == 1)
            
    for name, holiday_plans in worker_dict.items():
        for shift, _ in enumerate(holiday_plans):
            worker_var = getWorkerVar(name, shift)
            if(worker_var is None):
                continue            
            linExpr = [ getWorkIdVar(name, shift, i) for i in range(n_worker[shift]) ]
            problem.addConstraint(constraint= sum(linExpr) == worker_var)
    
    for name, holiday_plans in worker_dict.items():
        shift_size = len(holiday_plans)
        for shift in range(shift_size - 1):
            worker_var2, worker_var1 = getWorkerVar(name, shift + 1), getWorkerVar(name, shift)
            if(worker_var1 is not None and worker_var2 is not None):
                problem.addConstraint(constraint=worker_var1 + worker_var2 <= 1)        
    return 

#目的関数を設定
def setObjective(worker_dict : dict[str, list]):
    global problem

    for name, holiday_plans in worker_dict.items():
        for shift, holiday_plan in enumerate(holiday_plans):
            if(holiday_plan == "-1"):
                continue
            if(holiday_plan == "1"):                
                problem += -100 * getWorkerVar(name, shift)
    
    return 

def main() -> None:
    global problem
    input = read_input("./sample_input.csv")
    
    n_worker = [int(s) for s in input.pop("n_workers")]
    worker_dict = input

    create_variables(worker_dict, n_worker)
    setObjective(worker_dict)    

    create_cons(worker_dict, n_worker)

    problem.solve()

    output("./sample_output.csv", worker_dict)
    print("Status:", pulp.LpStatus[problem.status])

    return 

main()
