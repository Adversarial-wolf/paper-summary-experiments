import os 
import json
from matplotlib.lines import Line2D
import numpy as np
import matplotlib.pyplot as plt

list_N_trees = [10]
list_epsilon = [0.1, 1, 5, 10, 20, 30, 1000]
list_obj_active = [1]
list_depth = [5]
list_seed = [0,1,2,3,4,5,6,7,8,9]
list_datasets = ['compas' ,'default_credit', 'adult']
target_ratio_divisor = "0.050"

for N_samples in [100, 500, 1000, 2000, 5000, 10000, 20000]:
    i = 0
    results_per_dataset = {}
    dataset_medoid_baseline = {'adult': 0.19382631578947365, 'compas': 0.19321428571428573, 'default_credit': 0.3165333333333333}
    for N_trees in list_N_trees:
        for epsilon in list_epsilon: 
            for obj_active_bool in list_obj_active:
                for depth in list_depth:
                    for dataset in list_datasets:
                        if dataset == 'compas' and N_samples != 2000:
                            continue
                        if dataset == 'adult' and N_samples != 20000:
                            continue
                        if dataset == 'default_credit' and N_samples != 10000:
                            continue
                        for seed in list_seed:
                            # Load the corresponding simple informed adversary results
                            if N_samples == 100:
                                filename = "N_fixed%d_%.2f_%d_%d_%s_results.json" %(N_trees, epsilon, seed, depth, dataset) 
                            else:
                                filename = "N_fixed%d_%.2f_%d_%d_%d_%s_results.json" %(N_trees, epsilon, seed, depth, N_samples, dataset)
                            with open(os.path.join("experiments_results/Results_informed_adversary_balle", filename), 'r') as f:
                                result_simple = json.load(f)[0]
                                #print("Loaded simple informed adversary results file:", filename)
                            
                            if dataset not in results_per_dataset:
                                    results_per_dataset[dataset] = {
                                        'epsilon': [],
                                        'indiv_recon_error': {},
                                        'all_recon_error': [],
                                        'indiv_recon_error_simple': [],
                                        'duration_avg': {},
                                        'outliers_avg_reconstr': {},
                                        'inliers_avg_reconstr': {},
                                        'outliers_avg_reconstr_baseline': [],
                                        'inliers_avg_reconstr_baseline': [],
                                        'outliers_nb_perfect_baseline': [],
                                        'inliers_nb_perfect_baseline': [],
                                        'outliers_nb_perfect': {},
                                        'inliers_nb_perfect': {}
                                    }
                            train_accuracy_simple = result_simple['accuracy_train']
                            test_accuracy_simple = result_simple['accuracy_test']
                            #all_recon_error = result_main['reconstruction_error']
                            indiv_recon_error_simple = result_simple['example_reconstruction_error_avg']
                            results_per_dataset[dataset]['epsilon'].append(epsilon)
                            results_per_dataset[dataset]['indiv_recon_error_simple'].append(indiv_recon_error_simple)
                            i += 1

                            # Load the informed adversary (ours) results
                            if N_samples == 100:
                                filename = "N_fixed%d_%.2f_%d_%d_%s_%s_results.json" %(N_trees, epsilon, seed, depth, target_ratio_divisor, dataset) 
                            else:
                                filename = "N_fixed%d_%.2f_%d_%d_%s_%d_%s_results.json" %(N_trees, epsilon, seed, depth, target_ratio_divisor, N_samples, dataset) 
                            
                            with open(os.path.join("experiments_results/Results_informed_adversary", filename), 'r') as f:
                                result = json.load(f)[0]
                                #print("Loaded informed adversary results file:", filename)
                            
                            target_ratio_divisor_ = result['target_ratio_divisor']
                            assert(float(target_ratio_divisor_) == float(target_ratio_divisor)), "Target ratio divisors do not match!"
                            epsilon = result['epsilon']
                            train_accuracy = result['accuracy_train']
                            test_accuracy = result['accuracy_test']
                            indiv_recon_error = result['example_reconstruction_error_avg']
                            duration_avg = result['duration_avg']
                            dataset = os.path.splitext(os.path.basename(result['dataset']))[0]
                                # Make sure the results correspond to the same DP RFs
                            #assert result_main['epsilon'] == epsilon, "Epsilon values do not match!"
                            assert result_simple['epsilon'] == epsilon, "Epsilon values do not match!"

                            outliers = np.where(np.asarray(result["all_distances_outlier_scores"]) <= 0)
                            inliers = np.where(np.asarray(result["all_distances_outlier_scores"]) > 0)
                            outliers_avg = np.average(np.asarray(result["example_reconstruction_error_list"])[outliers])
                            inliers_avg = np.average(np.asarray(result["example_reconstruction_error_list"])[inliers])

                            outliers_avg_baseline = np.average(np.asarray(result_simple["example_reconstruction_error_list"])[outliers])
                            inliers_avg_baseline = np.average(np.asarray(result_simple["example_reconstruction_error_list"])[inliers])
                            results_per_dataset[dataset]['outliers_avg_reconstr_baseline'].append(outliers_avg_baseline)
                            results_per_dataset[dataset]['inliers_avg_reconstr_baseline'].append(inliers_avg_baseline)

                            outliers_prop_perfect_reconstr = 100*(list(np.asarray(result["example_reconstruction_error_list"])[outliers]).count(0) / len(outliers[0])) # percentage
                            inliers_prop_perfect_reconstr = 100*(list(np.asarray(result["example_reconstruction_error_list"])[inliers]).count(0) / len(inliers[0])) # percentage
                           
                            outliers_prop_perfect_reconstr_baseline = 100*(list(np.asarray(result_simple["example_reconstruction_error_list"])[outliers]).count(0) / len(outliers[0])) # percentage
                            inliers_prop_perfect_reconstr_baseline = 100*(list(np.asarray(result_simple["example_reconstruction_error_list"])[inliers]).count(0) / len(inliers[0])) # percentage
                            results_per_dataset[dataset]['outliers_nb_perfect_baseline'].append(outliers_prop_perfect_reconstr_baseline)
                            results_per_dataset[dataset]['inliers_nb_perfect_baseline'].append(inliers_prop_perfect_reconstr_baseline)

                            if train_accuracy_simple != train_accuracy or test_accuracy_simple != test_accuracy:
                                print("Warning: Train/Test accuracies do not match between informed adversary and simple informed adversary for file:", filename)

                            if target_ratio_divisor not in results_per_dataset[dataset]['indiv_recon_error']:
                                results_per_dataset[dataset]['indiv_recon_error'][target_ratio_divisor] = []
                                results_per_dataset[dataset]['duration_avg'][target_ratio_divisor] = []
                                results_per_dataset[dataset]["outliers_avg_reconstr"][target_ratio_divisor] = []
                                results_per_dataset[dataset]["inliers_avg_reconstr"][target_ratio_divisor] = []
                                results_per_dataset[dataset]["outliers_nb_perfect"][target_ratio_divisor] = []
                                results_per_dataset[dataset]["inliers_nb_perfect"][target_ratio_divisor] = []

                            results_per_dataset[dataset]['indiv_recon_error'][target_ratio_divisor].append(indiv_recon_error)
                            results_per_dataset[dataset]['duration_avg'][target_ratio_divisor].append(duration_avg)
                            results_per_dataset[dataset]["outliers_avg_reconstr"][target_ratio_divisor].append(outliers_avg)
                            results_per_dataset[dataset]["inliers_avg_reconstr"][target_ratio_divisor].append(inliers_avg)
                            #results_per_dataset[dataset]['all_recon_error'].append(all_recon_error)
                            results_per_dataset[dataset]['outliers_nb_perfect'][target_ratio_divisor].append(outliers_prop_perfect_reconstr)
                            results_per_dataset[dataset]['inliers_nb_perfect'][target_ratio_divisor].append(inliers_prop_perfect_reconstr)


                            i += 1

    print("[N_samples %d] Total number of result files processed: %d" % (N_samples, i))

    j = 0
    for dataset in results_per_dataset.keys():
        list_eps = results_per_dataset[dataset]['epsilon']
        list_indiv = results_per_dataset[dataset]['indiv_recon_error'][target_ratio_divisor]
        durations = results_per_dataset[dataset]['duration_avg'][target_ratio_divisor]
        list_indiv_outliers = results_per_dataset[dataset]['outliers_avg_reconstr'][target_ratio_divisor]
        list_indiv_inliers = results_per_dataset[dataset]['inliers_avg_reconstr'][target_ratio_divisor]
        list_indiv_outliers_baseline = results_per_dataset[dataset]['outliers_avg_reconstr_baseline']
        list_indiv_inliers_baseline = results_per_dataset[dataset]['inliers_avg_reconstr_baseline']
        list_perfect_outliers = results_per_dataset[dataset]['outliers_nb_perfect'][target_ratio_divisor]
        list_perfect_inliers = results_per_dataset[dataset]['inliers_nb_perfect'][target_ratio_divisor]
        list_perfect_outliers_baseline = results_per_dataset[dataset]['outliers_nb_perfect_baseline']
        list_perfect_inliers_baseline = results_per_dataset[dataset]['inliers_nb_perfect_baseline']

        #list_all = results_per_dataset[dataset]['all_recon_error']
        list_indiv_simple = results_per_dataset[dataset]['indiv_recon_error_simple']

        # Average errors that correspond to the same epsilon
        unique_epsilons = sorted(set(list_eps))
        avg_indiv_errors = []
        avg_all_errors = []
        std_indiv_errors = []
        std_all_errors = []
        avg_indiv_simple = []
        std_indiv_simple = []
        avg_indiv_outliers = []
        std_indiv_outliers = []
        avg_indiv_inliers = []
        std_indiv_inliers = []
        avg_indiv_outliers_baseline = []
        std_indiv_outliers_baseline = []
        avg_indiv_inliers_baseline = []
        std_indiv_inliers_baseline = []
        avg_indiv_perfect_outliers = []
        std_indiv_perfect_outliers = []
        avg_indiv_perfect_inliers = []
        std_indiv_perfect_inliers = []
        avg_indiv_perfect_outliers_baseline = []
        std_indiv_perfect_outliers_baseline = []    
        avg_indiv_perfect_inliers_baseline = []
        std_indiv_perfect_inliers_baseline = []
        print("Global duration avg = ", np.mean(durations), " over ", len(durations), " runs.")
        for eps in unique_epsilons:
            indices = [index for index, value in enumerate(list_eps) if value == eps]
            assert(len(indices) == len(list_seed))  # seeds
            
            avg_indiv_errors.append(np.mean([list_indiv[index] for index in indices]))
            #avg_all_errors.append(avg_all)
            std_indiv_errors.append(np.std([list_indiv[index] for index in indices]))
            #std_all_errors.append(np.std([list_all[index] for index in indices]))

            avg_indiv_simple.append(np.mean([list_indiv_simple[index] for index in indices]))
            std_indiv_simple.append(np.std([list_indiv_simple[index] for index in indices]))

            avg_indiv_outliers.append(np.mean([list_indiv_outliers[index] for index in indices]))
            std_indiv_outliers.append(np.std([list_indiv_outliers[index] for index in indices]))

            avg_indiv_inliers.append(np.mean([list_indiv_inliers[index] for index in indices]))
            std_indiv_inliers.append(np.std([list_indiv_inliers[index] for index in indices]))

            avg_indiv_outliers_baseline.append(np.mean([list_indiv_outliers_baseline[index] for index in indices]))
            std_indiv_outliers_baseline.append(np.std([list_indiv_outliers_baseline[index] for index in indices]))

            avg_indiv_inliers_baseline.append(np.mean([list_indiv_inliers_baseline[index] for index in indices]))
            std_indiv_inliers_baseline.append(np.std([list_indiv_inliers_baseline[index] for index in indices]))

            avg_indiv_perfect_outliers.append(np.mean([list_perfect_outliers[index] for index in indices]))
            std_indiv_perfect_outliers.append(np.std([list_perfect_outliers[index] for index in indices]))  

            avg_indiv_perfect_inliers.append(np.mean([list_perfect_inliers[index] for index in indices]))
            std_indiv_perfect_inliers.append(np.std([list_perfect_inliers[index] for index in indices]))

            avg_indiv_perfect_outliers_baseline.append(np.mean([list_perfect_outliers_baseline[index] for index in indices]))
            std_indiv_perfect_outliers_baseline.append(np.std([list_perfect_outliers_baseline[index] for index in indices]))

            avg_indiv_perfect_inliers_baseline.append(np.mean([list_perfect_inliers_baseline[index] for index in indices]))
            std_indiv_perfect_inliers_baseline.append(np.std([list_perfect_inliers_baseline[index] for index in indices]))  


        plt.figure()
        #plt.title(f"Reconstruction Error vs Epsilon for {dataset}")
        plt.xlabel(r"$\epsilon$") 
        plt.ylabel("Reconstruction Error")

        plt.axhline(y=dataset_medoid_baseline[dataset], color='red', linestyle='--', label='Simple per-coordinate majority baseline')
        
        plt.plot(unique_epsilons, avg_indiv_errors, marker='o', label='Informed Adversary', color='blue')
        plt.fill_between(
            unique_epsilons,
            np.array(avg_indiv_errors) - np.array(std_indiv_errors),
            np.array(avg_indiv_errors) + np.array(std_indiv_errors),
            alpha=0.2, color='blue'
        )
        
        plt.plot(unique_epsilons, avg_indiv_simple, marker='s', label='Informed Adversary Baseline [47]', color='green')
        plt.fill_between(
            unique_epsilons,
            np.array(avg_indiv_simple) - np.array(std_indiv_simple),
            np.array(avg_indiv_simple) + np.array(std_indiv_simple),
            alpha=0.2, color='green'
        )
        plt.xscale('log')

        plt.grid()
        plt.savefig(f"figures/reconstruction_error_informed_adversary_{dataset}_{N_samples}_{str(float(target_ratio_divisor))}.pdf", bbox_inches='tight')
        print("Plot saved:", f"figures/reconstruction_error_informed_adversary_{dataset}_{N_samples}_{target_ratio_divisor}.pdf")
        plt.close()
        j += 1

        # Inliers/Outliers plots
        plt.figure()
        #plt.title(f"Reconstruction Error vs Epsilon for {dataset}")
        plt.xlabel(r"$\epsilon$") 
        plt.ylabel("Reconstruction Error")

        plt.axhline(y=dataset_medoid_baseline[dataset], color='red', linestyle='--', label='Simple per-coordinate majority baseline')

        plt.plot(unique_epsilons, avg_indiv_outliers, marker="v", label='Informed Adversary (outliers)', color='dodgerblue', linestyle='dashdot')
        plt.fill_between(
            unique_epsilons,
            np.array(avg_indiv_outliers) - np.array(std_indiv_outliers),
            np.array(avg_indiv_outliers) + np.array(std_indiv_outliers),
            alpha=0.2, color='dodgerblue'
        )

        plt.plot(unique_epsilons, avg_indiv_inliers, marker='^', label='Informed Adversary (inliers)', color='darkblue', linestyle='dotted')
        plt.fill_between(
            unique_epsilons,
            np.array(avg_indiv_inliers) - np.array(std_indiv_inliers),
            np.array(avg_indiv_inliers) + np.array(std_indiv_inliers),
            alpha=0.2, color='darkblue'
        )
        plt.xscale('log')

        plt.grid()
        plt.savefig(f"figures/reconstruction_error_informed_adversary_{dataset}_{N_samples}_{str(float(target_ratio_divisor))}_outliers_ours.pdf", bbox_inches='tight')
        print("Plot saved:", f"figures/reconstruction_error_informed_adversary_{dataset}_{N_samples}_{target_ratio_divisor}_outliers_ours.pdf")
        plt.close()

        j += 1

        # Inliers/Outliers plots (baseline)
        plt.figure()
        #plt.title(f"Reconstruction Error vs Epsilon for {dataset}")
        plt.xlabel(r"$\epsilon$") 
        plt.ylabel("Reconstruction Error")

        plt.axhline(y=dataset_medoid_baseline[dataset], color='red', linestyle='--', label='Simple per-coordinate majority baseline')

        plt.plot(unique_epsilons, avg_indiv_outliers_baseline, marker="v", label='Informed Adversary Baseline [47] (outliers)', color='lime', linestyle='dashdot')
        plt.fill_between(
            unique_epsilons,
            np.array(avg_indiv_outliers_baseline) - np.array(std_indiv_outliers_baseline),
            np.array(avg_indiv_outliers_baseline) + np.array(std_indiv_outliers_baseline),
            alpha=0.2, color='lime'
        )

        plt.plot(unique_epsilons, avg_indiv_inliers_baseline, marker='^', label='Informed Adversary Baseline [47] (inliers)', color='darkgreen', linestyle='dotted')
        plt.fill_between(
            unique_epsilons,
            np.array(avg_indiv_inliers_baseline) - np.array(std_indiv_inliers_baseline),
            np.array(avg_indiv_inliers_baseline) + np.array(std_indiv_inliers_baseline),
            alpha=0.2, color='darkgreen'
        )
        plt.xscale('log')

        plt.grid()
        plt.savefig(f"figures/reconstruction_error_informed_adversary_{dataset}_{N_samples}_{str(float(target_ratio_divisor))}_outliers_baseline.pdf", bbox_inches='tight')
        print("Plot saved:", f"figures/reconstruction_error_informed_adversary_{dataset}_{N_samples}_{target_ratio_divisor}_outliers_baseline.pdf")
        plt.close()

        j += 1

        # Inliers/Outliers nb perfectplots
        plt.figure()
        #plt.title(f"Reconstruction Error vs Epsilon for {dataset}")
        plt.xlabel(r"$\epsilon$") 
        plt.ylabel("Proportion of perfect reconstructions (%)")

        plt.plot(unique_epsilons, avg_indiv_perfect_outliers, marker="v", label='Informed Adversary (outliers)', color='dodgerblue', linestyle='dashdot')
        plt.fill_between(
            unique_epsilons,
            np.array(avg_indiv_perfect_outliers) - np.array(std_indiv_perfect_outliers),
            np.array(avg_indiv_perfect_outliers) + np.array(std_indiv_perfect_outliers),
            alpha=0.2, color='dodgerblue'
        )

        plt.plot(unique_epsilons, avg_indiv_perfect_inliers, marker='^', label='Informed Adversary (inliers)', color='darkblue', linestyle='dotted')
        plt.fill_between(
            unique_epsilons,
            np.array(avg_indiv_perfect_inliers) - np.array(std_indiv_perfect_inliers),
            np.array(avg_indiv_perfect_inliers) + np.array(std_indiv_perfect_inliers),
            alpha=0.2, color='darkblue'
        )
        plt.xscale('log')

        plt.grid()
        plt.savefig(f"figures/reconstruction_error_informed_adversary_{dataset}_{N_samples}_{str(float(target_ratio_divisor))}_outliers_nb_perfect_ours.pdf", bbox_inches='tight')
        print("Plot saved:", f"figures/reconstruction_error_informed_adversary_{dataset}_{N_samples}_{target_ratio_divisor}_outliers_nb_perfect_ours.pdf")
        plt.close()

        j += 1

        # Inliers/Outliers nb perfect plots (baseline)
        plt.figure()
        #plt.title(f"Reconstruction Error vs Epsilon for {dataset}")
        plt.xlabel(r"$\epsilon$") 
        plt.ylabel("Proportion of perfect reconstructions (%)")

        plt.plot(unique_epsilons, avg_indiv_perfect_outliers_baseline, marker="v", label='Informed Adversary Baseline [47] (outliers)', color='lime', linestyle='dashdot')
        plt.fill_between(
            unique_epsilons,
            np.array(avg_indiv_perfect_outliers_baseline) - np.array(std_indiv_perfect_outliers_baseline),
            np.array(avg_indiv_perfect_outliers_baseline) + np.array(std_indiv_perfect_outliers_baseline),
            alpha=0.2, color='lime'
        )

        plt.plot(unique_epsilons, avg_indiv_perfect_inliers_baseline, marker='^', label='Informed Adversary Baseline [47] (inliers)', color='darkgreen', linestyle='dotted')
        plt.fill_between(
            unique_epsilons,
            np.array(avg_indiv_perfect_inliers_baseline) - np.array(std_indiv_perfect_inliers_baseline),
            np.array(avg_indiv_perfect_inliers_baseline) + np.array(std_indiv_perfect_inliers_baseline),
            alpha=0.2, color='darkgreen'
        )
        plt.xscale('log')

        plt.grid()
        plt.savefig(f"figures/reconstruction_error_informed_adversary_{dataset}_{N_samples}_{str(float(target_ratio_divisor))}_outliers_nb_perfect_baseline.pdf", bbox_inches='tight')
        print("Plot saved:", f"figures/reconstruction_error_informed_adversary_{dataset}_{N_samples}_{target_ratio_divisor}_outliers_nb_perfect_baseline.pdf")
        plt.close()

        j += 1


    print("Total number of plots generated:", j)

    # Separate legend
    legend_elements = []
    legend_elements.append(Line2D([0], [0], marker='s', label='Informed adversary baseline (adapted from [47])', color='green' )) #lw=5, 
    legend_elements.append(Line2D([0], [0], marker=None, color='red', linestyle='--', label='Simple per-coordinate majority baseline')) #lw=5, 
    legend_elements.append(Line2D([0], [0], marker='o', label='Informed adversary (ours)', color='blue' )) #lw=5, 

    
    legendFig = plt.figure(figsize=(2, 2))
    ax = legendFig.add_subplot(111)
    ax.axis('off')

    legend = ax.legend(handles=legend_elements, loc='center', ncol=1)

    legendFig.canvas.draw()
    bbox = legend.get_window_extent().transformed(legendFig.dpi_scale_trans.inverted())

    plt.axis('off')
    legendFig.savefig('figures/plot_informed_experiments_legend.pdf', bbox_inches='tight', pad_inches=0)
    plt.close()

    # Separate legend (outliers/inliers (ours))
    legend_elements = []
    legend_elements.append(Line2D([0], [0], marker='v', label='Informed adversary (ours) - Outliers', color='dodgerblue', linestyle='dashdot' )) #lw=5, 
    legend_elements.append(Line2D([0], [0], marker='^', label='Informed adversary (ours) - Inliers', color='darkblue', linestyle='dotted' )) #lw=5, 
    legend_elements.append(Line2D([0], [0], marker=None, color='red', linestyle='--', label='Simple per-coordinate majority baseline')) #lw=5, 

    
    legendFig = plt.figure(figsize=(2, 2))
    ax = legendFig.add_subplot(111)
    ax.axis('off')

    legend = ax.legend(handles=legend_elements, loc='center', ncol=1)

    legendFig.canvas.draw()
    bbox = legend.get_window_extent().transformed(legendFig.dpi_scale_trans.inverted())

    plt.axis('off')
    legendFig.savefig('figures/plot_informed_experiments_legend_outliers_ours.pdf', bbox_inches='tight', pad_inches=0)
    plt.close()

    # Separate legend (outliers/inliers (baseline))
    legend_elements = []
    legend_elements.append(Line2D([0], [0], marker='v', label='Informed adversary baseline (adapted from [47]) - Outliers', color='lime', linestyle='dashdot')) #lw=5, 
    legend_elements.append(Line2D([0], [0], marker='^', label='Informed adversary baseline (adapted from [47]) - Inliers', color='darkgreen', linestyle='dotted' )) #lw=5, 
    legend_elements.append(Line2D([0], [0], marker=None, color='red', linestyle='--', label='Simple per-coordinate majority baseline')) #lw=5, 

    
    legendFig = plt.figure(figsize=(2, 2))
    ax = legendFig.add_subplot(111)
    ax.axis('off')

    legend = ax.legend(handles=legend_elements, loc='center', ncol=1)

    legendFig.canvas.draw()
    bbox = legend.get_window_extent().transformed(legendFig.dpi_scale_trans.inverted())

    plt.axis('off')
    legendFig.savefig('figures/plot_informed_experiments_legend_outliers_baseline.pdf', bbox_inches='tight', pad_inches=0)
    plt.close()

    # Separate legend (outliers/inliers (ours)) - nb perfect
    legend_elements = []
    legend_elements.append(Line2D([0], [0], marker='v', label='Informed adversary (ours) - Outliers', color='dodgerblue', linestyle='dashdot' )) #lw=5, 
    legend_elements.append(Line2D([0], [0], marker='^', label='Informed adversary (ours) - Inliers', color='darkblue', linestyle='dotted' )) #lw=5, 
    
    legendFig = plt.figure(figsize=(2, 2))
    ax = legendFig.add_subplot(111)
    ax.axis('off')

    legend = ax.legend(handles=legend_elements, loc='center', ncol=1)

    legendFig.canvas.draw()
    bbox = legend.get_window_extent().transformed(legendFig.dpi_scale_trans.inverted())

    plt.axis('off')
    legendFig.savefig('figures/plot_informed_experiments_legend_outliers_ours_nb_perfect.pdf', bbox_inches='tight', pad_inches=0)
    plt.close()

    # Separate legend (outliers/inliers (baseline)) - nb perfect
    legend_elements = []
    legend_elements.append(Line2D([0], [0], marker='v', label='Informed adversary baseline (adapted from [47]) - Outliers', color='lime', linestyle='dashdot')) #lw=5, 
    legend_elements.append(Line2D([0], [0], marker='^', label='Informed adversary baseline (adapted from [47]) - Inliers', color='darkgreen', linestyle='dotted' )) #lw=5, 
    
    legendFig = plt.figure(figsize=(2, 2))
    ax = legendFig.add_subplot(111)
    ax.axis('off')

    legend = ax.legend(handles=legend_elements, loc='center', ncol=1)

    legendFig.canvas.draw()
    bbox = legend.get_window_extent().transformed(legendFig.dpi_scale_trans.inverted())

    plt.axis('off')
    legendFig.savefig('figures/plot_informed_experiments_legend_outliers_baseline_nb_perfect.pdf', bbox_inches='tight', pad_inches=0)
    plt.close()

    
