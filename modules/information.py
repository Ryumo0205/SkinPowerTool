#!/usr/bin/env python
# -*-coding:utf-8 -*-
import maya.cmds as cmds
import pymel.core as pm


class Info:

    def __init__(self):
        self.reset_info()

    def reset_info(self):
        """
        Resets all properties to None. This will effectively clear any previous state.
        """
        # Using a dictionary and iteration to reinitialize all attributes
        for attr in ['display_inf_list', 'display_weights_list', 'weights_list', 
                     'current_dict', 'selected_vertices', 'mesh_name', 
                     'skin_clusters', 'all_influences']:
            setattr(self, attr, None)

    def update_info(self):
        """
        Updates the information of the selected vertices, mesh name, skin clusters, and influences.
        
        Returns:
            bool: True if info was successfully updated, False otherwise.
        """
        
        selected = cmds.ls(selection=True, flatten=True)
        if not selected:
            
            self.reset_info()
            return False

        selected_type = cmds.objectType(selected[0])
        if selected_type == "mesh":
            self.selected_vertices = selected
            self.mesh_name = self.selected_vertices[0].split('.')[0]
            history = cmds.listHistory(self.mesh_name)
            self.skin_clusters = cmds.ls(history, type='skinCluster')[0] if history else None

            if not self.skin_clusters:
                
                self.reset_info()
                return False

            self.all_influences = pm.skinPercent(self.skin_clusters, 
                                                 self.selected_vertices, 
                                                 query=True, transform=None)
            self.update_weights_data()
            
            return True
        else:
            
            self.reset_info()
            return False

    def update_weights_data(self):
        """
        Collects the weighting information for all influences on the selected vertices.
        """
        weights_data = {i: [] for i in self.all_influences}
        influences_with_weight = set()

        for vertex in self.selected_vertices:
            weights = pm.skinPercent(self.skin_clusters, vertex, query=True, value=True)
            for influence, weight in zip(self.all_influences, weights):
                if weight > 0:
                    influences_with_weight.add(influence)
                    weights_data[influence].append(weight)

        self.display_inf_list = sorted(influences_with_weight, key=self.all_influences.index)
        self.current_dict = {inf: max(weights) for inf, weights in weights_data.items() if weights}
        self.weights_list = [max(weights_data[inf]) if weights_data[inf] else 0 for inf in self.all_influences]
        self.display_weights_list = [round(w, 2) for w in self.weights_list if w > 0]

    def search_joints(self, query):

        results = [s for s in self.all_influences if query.lower()
                   in s.lower()]
        return results


if __name__ == "__main__":
    pass
else:
    info = Info()