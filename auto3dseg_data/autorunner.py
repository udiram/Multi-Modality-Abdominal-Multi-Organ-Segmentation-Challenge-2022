from monai.apps.auto3dseg import AutoRunner

if __name__ == '__main__':
    runner = AutoRunner(input={"name": "Task500_AMOS",
                                "task": "segmentation",
                                "modality": "CT",
                                "datalist": "datalist.json",
                                "dataroot": "data",},
                        work_dir="work_dir/",
                        analyze=True,
                        algo_gen=True, 
                        algos=['segresnet'])
                        
    runner.set_training_params({"cache_rate": 0.1})
    runner.run()
