from __future__ import absolute_import
from aether.dataobjects.SpacetimeDynamic import SpacetimeDynamic
import aether as ae
import numpy as np
import functools
from six.moves import range


class satellite(object):

    @staticmethod
    def LandSatMasks(builder, sky, qa_index):
        spacetime = SpacetimeDynamic(builder, sky)
        qa_band = spacetime.bands(ts=None, bands=qa_index)

        masks_arr, labels_arr = [], []
        for ts_i in range(len(builder.timestamps)):
            spacecraft_id, sensor_id, collection = ae.contrib.logic.landsat.parse_sb_to_return_meta(builder, ts_i, qa_index)
            m, l = ae.contrib.logic.landsat.landsat_qa_band(np.expand_dims(qa_band[ts_i], axis=0), spacecraft_id, sensor_id, collection)
            masks_arr.append(m)
            labels_arr.append(l)

        # Regularize this mask. This preserves the order of the labels.
        labels = []
        for arr in labels_arr:
            for l in arr:
                if l not in labels:
                    labels.append(l)
        masks = np.zeros(qa_band.shape[0:3] + (len(labels),))
        for ts_i in range(len(builder.timestamps)):
            its_labels = labels_arr[ts_i]
            for l_i, label in enumerate(its_labels):
                out_i = labels.index(label)
                masks[ts_i,:,:,out_i] = masks_arr[ts_i][:,:,:,l_i]
        return masks, labels