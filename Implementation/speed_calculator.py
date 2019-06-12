import fiona
import geopy.distance as ds
import geopandas as gpd

'''def radius(coordinates):
    with fiona.open('./shapefiles/como_points.shp') as file:
        for point in file:
            distances, indices = tree.query(point, len(points), p=2, distance_upper_bound=max_distance)
    point_neighbors = []
    for index, distance in zip(indices, distances):
        if distance == inf:
            break
        point_neighbors.append(points[index])
    point_neighbors_list.append(point_neighbors)
        for ft in file:'''
            
        
    
with fiona.open('./shapefiles/speedy_Como_dataset.shp') as np:
    meta = np.meta
    timezones = []
    print("Recupero time_zones...")
    for feature in np:
        # aggiungo colonna speed
        feature['properties']['speed'] = 'float'
        #recupero tutti i timezone e li salvo in una lista
        timezone = feature['properties']['time_zone']
        if timezone not in timezones:
            timezones.append(timezone)

    print("Stampo i path...")
    paths = []
    n = 0
    for tz in timezones:
        print("Percorso " + str(n))
        n += 1
        path = filter(lambda f: f['properties']['time_zone'] == tz, np)
        path = list(path)
        # print(path[0])
        # esempio struttura
        # {'type': 'Feature', 'id': '0', 'properties': OrderedDict([('ts', 1460114897392.0), ('time_zone', '2016-04-08 11:28:14.000000'), ('location', 'Como'), ('latitude', 45.80360806110678), ('longitude', 9.094291062725679), ('tr_point', '0101000020E61000007B6C0DEB46302240B7A002A1DCE64640')]), 'geometry': {'type': 'Point', 'coordinates': (9.094291062725679, 45.80360806110678)}}
        prev_geom = None
        prev_time = 0.0
        duration=0
        for i in range(len(path)):
            
            curr_geom = path[i]['geometry']['coordinates']
            curr_time = path[i]['properties']['ts']
            distance = 0.0
            speed = 0.0
            s_tot=0.0            
            if i > 0:
                distance = ds.distance(curr_geom, prev_geom).meters
                speed = distance / ((curr_time - prev_time) / 1000)
                s_tot=s_tot+speed
                duration+=(curr_time-prev_time)/1000
            if i==(len(path)-1):
                speed_avg=s_tot/i
                path[i]['properties']['end_point'] = curr_geom                
                path[i]['properties']['speed_avg'] = speed_avg
                path[i]['properties']['start_point'] = curr_geom
                if (speed_avg>0 and speed_avg<=2.3):
                    path[i]['properties']['type'] = 'foot'
                elif (speed_avg>2.3):
                    path[i]['properties']['type'] = 'drive'
                path[i]['properties']['duration'] = duration
            path[i]['properties']['speed'] = speed
            prev_geom = curr_geom
            prev_time = curr_time
            paths.append(path[i])
        # break

# print(paths)

gdf = gpd.GeoDataFrame.from_features(paths)

# gdf = gpd.GeoDataFrame(paths)
gdf.to_file(driver = 'ESRI Shapefile', filename = './shapefiles/speedy_Como_dataset2.shp')
