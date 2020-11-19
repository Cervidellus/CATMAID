(function(CATMAID) {

  'use strict';

  // Map transaction operations to more userfriendly labels
  CATMAID.TransactionOperations = {
    "annotations.add": "Add annotation",
    "annotations.remove": "Remove annotations",
    "textlabels.create": "Create text label",
    "textlabels.remove": "Remove text label",
    "textlabels.update": "Update text label",
    "labels.update": "Add or update tags",
    "labels.remove": "Remove tag",
    "labels.remove_unused": "Remove unused labels",
    "links.create": "Create connector link",
    "links.remove": "Remove connector link",
    "connectors.create": "Create connector",
    "connectors.remove": "Remove connector",
    "neurons.give_to_user": "Give neuron to user",
    "neurons.remove": "Remove neuron",
    "neurons.rename": "Rename neuron",
    "nodes.add_or_update_review": "Review node",
    "nodes.update_location": "Update node location",
    "treenodes.create": "Create treenode",
    "treenodes.insert": "Insert treenode",
    "treenodes.remove": "Remove treenode",
    "treenodes.update_confidence": "Update treenode confidence",
    "treenodes.update_parent": "Update treenode parent",
    "treenodes.update_radius": "Update treenode radius",
    "treenodes.suppress_virtual_node": "Suppress virtual node",
    "treenodes.unsuppress_virtual_node": "Unsuppress virtual node",
    "skeletons.reset_own_reviews": "Reset own reviews in skeleton",
    "skeletons.split": "Split skeleton",
    "skeletons.merge": "Merge skeletons",
    "skeletons.reroot": "Reroot skeleton",
    "skeletons.import": "Import skeleton",
    "projects.clear_tags": "Clear tags on project",
    "projects.update_tags": "Update tags on project",
    "stacks.clear_tags": "Clear tags on stack",
    "stacks.update_tags": "Update tags on stacks",
    "ontologies.add_relation": "Add ontology relation",
    "ontologies.rename_relation": "Rename ontology relation",
    "ontologies.remove_relation": "Remove ontology relation",
    "ontologies.remove_all_relations": "Remove all ontology relations",
    "ontologies.add_class": "Add ontology class",
    "ontologies.rename_class": "Rename ontology class",
    "ontologies.remove_class": "Remove ontology class",
    "ontologies.remove_all_classes": "Remove all ontology classes",
    "ontologies.add_link": "Add ontology link",
    "ontologies.remove_link": "Add ontology link",
    "ontologies.remove_all_links": "Remove all ontology links",
    "ontologies.add_restriction": "Add ontology restriction",
    "ontologies.remove_restriction": "Remove ontology restriction",
    "classifications.rebuild_env": "Rebuild classification environment for project",
    "classifications.add_graph": "Add classification graph",
    "classifications.remove_graph": "Remove classification graph",
    "classifications.update_graph": "Update classification graph",
    "classifications.autofill_graph": "Auto-fill classification graph",
    "classifications.link_graph": "Link classification graph",
    "classifications.link_roi": "Link ROI into classification graph",
    "change_requests.approve": "Approve change request",
    "change_requests.reject": "Reject change request",
    "rois.create_link": "Link ROI",
    "rois.remove_link": "Remove link to ROI",
    "rois.create": "Add ROI",
    "clusterings.setup_env": "Rebuild clustering environment for project",
    "volumes.create": "Create volume"
  };

})(CATMAID);
