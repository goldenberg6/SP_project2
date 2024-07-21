import sys
import pandas as pd
import numpy as np


def validate_args():
    if len(sys.argv[1:]) == 5:
        try:
            k = sys.argv[1]
            k = float(k)
            if k % 1 != 0:
                exit()
            k = int(k)
        except:
            print("Invalid number of clusters!")
            exit()
        try:
            itr = sys.argv[2]
            itr = float(itr)
            if itr % 1 != 0:
                exit()
            itr = int(itr)
            if itr <= 1 or itr >= 1000:
                exit()
        except:
            print("Invalid maximum iteration!")
            exit()

        try:
            eps = sys.argv[3]
            eps = float(eps)
            if eps < 0:
                exit()
        except:
            print("Invalid epsilon!")
            exit()
        file_name_1 = sys.argv[4]
        file_name_2 = sys.argv[5]
    elif len(sys.argv[1:]) == 4:
        try:
            k = sys.argv[1]
            k = float(k)
            if k % 1 != 0:
                exit()
            k = int(k)
        except:
            print("Invalid number of clusters!")
            exit()

        itr = 300

        try:
            eps = sys.argv[2]
            eps = float(eps)
            if eps < 0:
                exit()
        except:
            print("Invalid epsilon!")
            exit()

        file_name_1 = sys.argv[3]
        file_name_2 = sys.argv[4]
    else:
        print("An Error Has Occurred")
        exit()

    return k, itr, eps, file_name_1, file_name_2


def read_files(file_name_1, file_name_2):
    df1 = pd.read_csv(file_name_1, header=None, sep=',')
    df2 = pd.read_csv(file_name_2, header=None, sep=',')

    merged_df = pd.merge(df1, df2, on=0, how='inner')

    sorted_df = merged_df.sort_values(by=0)

    data_points = [list(row)[1:] for _, row in sorted_df.iterrows()]
    return data_points


def centroids_init(k, data_points):
    np.random.seed(1234)
    data_points_copy = data_points.copy()
    centroids_indices = []
    centroids = []
    relevant_indices = list(range(0, len(data_points)))

    # inserting first datat point
    first_centroid_index = np.random.choice(np.arange(0, len(data_points)))
    centroids_indices.append(first_centroid_index)
    centroids.append(data_points_copy[first_centroid_index])
    relevant_indices.remove(first_centroid_index)

    for i in range(1, k):
        distances = calc_dists(centroids, data_points_copy, relevant_indices)
        sum_of_dists = sum(distances)
        probabilities = [dist / sum_of_dists for dist in distances]
        new_centroid_index = np.random.choice(relevant_indices, p=probabilities)
        centroids_indices.append(new_centroid_index)
        centroids.append(data_points_copy[new_centroid_index])
        relevant_indices.remove(new_centroid_index)

    return centroids_indices


def calc_dists(centroids, data_points_copy, relevant_indices):
    distances = []
    for data_point_index in relevant_indices:
        # BUG?
        dist = np.min([np.linalg.norm(np.array(data_points_copy[data_point_index]) - np.array(centroid)) for centroid in
                       centroids])
        distances.append(dist)
    return distances


def main():
    try:
        k, itr, eps, file_name_1, file_name_2 = validate_args()
        data_points = read_files(file_name_1, file_name_2)
        if k <= 1 or k >= len(data_points):
            print("Invalid maximum iteration!")
            exit()
        init_centroids = [int(centroid) for centroid in centroids_init(k, data_points)]
        print(init_centroids)
    except:
        print("An Error Has Occurred")
        exit()


if __name__ == '__main__':
    main()
