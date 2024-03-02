#!/usr/bin/env python
# -*-coding:utf-8 -*-
from decimal import Decimal, ROUND_HALF_UP
from modules.information import info
import maya.cmds as cmds
import pymel.core as pm
import copy


class Edit:

    copied_weights = None

    def __init__(self):
        pass

    # DONE:

    def weight_set(self, input_pairs):
        """
        Directly specifies the weights of the vertices.
        The input_pairs parameter should be passed as a tuple type, accepting only a single tuple. 
        Providing multiple selections will cause normalization issues.
        example: ("joint1", 0.5), ("joint2", 0.5)
        """
        pm.skinPercent(info.skin_clusters, info.selected_vertices,
                       transformValue=input_pairs, normalize=True)

        info.update_weights_data()

    # DONE:

    def weight_plus(self, input_pairs):
        """
        Input a floating-point number and calculate the weight by addition.
        The input_pairs parameter should be passed as a tuple type, accepting only a single tuple. 
        Providing multiple selections will cause normalization issues.
        example: ("joint1", 0.1)
        This operation would result in the current weight of joint1 +0.1
        """
        joint, add_weight = input_pairs

        if joint in info.current_dict:  # Check if the joint exists in the info.current_dict dictionary

            new_weight = info.current_dict[joint] + add_weight
            final_tuple = (joint, new_weight)

        pm.skinPercent(info.skin_clusters, info.selected_vertices,
                       transformValue=final_tuple, normalize=True)

    # DONE:

    def weight_minus(self, input_pairs):
        """
        Input a floating-point number and calculate the weight by subtraction.
        The input_pairs parameter should be passed as a tuple type, accepting only a single tuple. 
        Providing multiple selections will cause normalization issues.
        example: ("joint1", 0.1)
        This operation would result in the current weight of joint1 -0.1
        """

        joint, subtract_weight = input_pairs
        if joint in info.current_dict:

            new_weight = info.current_dict[joint] - subtract_weight
            final_tuple = (joint, new_weight)

        pm.skinPercent(info.skin_clusters, info.selected_vertices,
                       transformValue=final_tuple, normalize=True)


    @classmethod
    def weight_copy(cls):
        """
        Copies the current vertex weight data and returns it.
        """
        cls.copied_weights = copy.deepcopy(info.current_dict)
        print("copied data : ", cls.copied_weights)
        return cls.copied_weights


    @classmethod
    def weight_paste(cls):
        """
        Operates directly to paste the copied data.
        """

        if cls.copied_weights is not None:

            combined_list = [(key, value)
                             for key, value in cls.copied_weights.items()]

            pm.skinPercent(info.skin_clusters, info.selected_vertices,
                           transformValue=combined_list, normalize=True)

        else:
            print("No weights have been copied yet.")

    def weight_smooth(self):

        """
        Smoothes the skin weights using Maya's built-in method.
        """        
        cmds.SmoothSkinWeights()


    def weight_mirror(self):

        """
        Mirrors the skin weights along the YZ plane, affecting only the selected vertices.
        """
        pm.copySkinWeights(mirrorMode="YZ", sampleSpace=1)

    def prune_weight(self, get_value):

        pm.skinPercent(info.skin_clusters, info.mesh_name,
                       pruneWeights=get_value)

    def round_weight(self, round_num):
        '''
        Rounds the skin weights to a specified number of decimal places.
        This process can be time-consuming for meshes with a high vertex count and numerous joints.

        '''
        gMainProgressBar = pm.mel.eval('$tmp = $gMainProgressBar')


        all_influences = info.all_influences    # all influence strings list
        vtx_list = info.selected_vertices       # all vertices numbers list
        skin_clusters = info.skin_clusters      # skin_clusters node name
        decimal_one = Decimal('1.00')
        round_num_list = ["0.1", "0.01", "0.001", "0.0001", "0.00001"]
        decimal_digit = Decimal(round_num_list[int(round_num) - 1])
        max_len = len(vtx_list)
        progress_interval = max_len // 20


        for index, vtx in enumerate(vtx_list):
            if index % progress_interval == 0:
                pm.progressBar( gMainProgressBar,
                    edit=True,
                    beginProgress=True,
                    isInterruptable=True,
                    status='Rounding...',
                    progress=index,
                    maxValue=max_len )
                
            
            
            weights_list = pm.skinPercent( skin_clusters, vtx, query=True, value=True)

            # must be use Decimal
            rounded_weights = [Decimal(str(w)).quantize(decimal_digit, rounding=ROUND_HALF_UP) for w in weights_list]
            sum_rounded_values = sum(rounded_weights)

            error = sum_rounded_values - decimal_one 

            if error != 0:
                # skip influences with zero weight.
                filtered_weights = {influence: weight for influence, weight in zip(
                    all_influences, rounded_weights) if weight > 0}
                max_key = max(filtered_weights, key=filtered_weights.get)
                min_key = min(filtered_weights, key=filtered_weights.get)

                # Adjust weights using the error. If the error is negative, add it to the smallest weight (convert error to positive), 
                # if it's positive, subtract it from the largest weight.
                if error < 0:
                    filtered_weights[min_key] += abs(error)
                else:
                    filtered_weights[max_key] -= error

                # Update rounded_weights
                for i, influence in enumerate(all_influences):
                    if influence in filtered_weights:
                        rounded_weights[i] = filtered_weights[influence]

            # Combine into tuples and place into a list, to be used as input for the skinPercent command.
            combine_list = [(inf, float(wt))
                            for inf, wt in zip(all_influences, rounded_weights)]
            pm.skinPercent(skin_clusters, vtx, transformValue=combine_list)

        

        


if __name__ == "__main__":
    pass
else:
    edit = Edit()
