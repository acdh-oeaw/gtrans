from browsing.browsing_utils import model_to_dict


def as_node(instance):
    """ serializes an object as netvis-nodes
        :param instance: An instance of a django model class
        :return: A dict with keys 'type', 'label' and 'id'
    """
    node = {}
    node["type"] = f"{instance.__class__.__name__}"
    node["label"] = f"{instance.__str__()}"
    node["id"] = f"{node['type'].lower()}__{instance.id}"
    return node


def as_graph(instance):
    """ serializes an object and its related (FK, M2M) objects as nevis-graph
        :param instance: An instance of a django model class
        :return: A dict with keys 'nodes' and 'edges'
    """
    obj_dict = model_to_dict(instance)
    graph = {
        'nodes': [as_node(instance)],
        'edges': []
    }

    for x in obj_dict:
        if x['f_type'] == 'FK' and x['value'] is not None:
            graph['nodes'].append(as_node(x['value']))
            graph['edges'].append(
                {
                    'id': f"{as_node(instance)['id']}__{as_node(x['value'])['id']}",
                    'source': as_node(instance)['id'],
                    'target': as_node(x['value'])['id'],
                    'label': x['verbose_name']
                }
            )
        elif x['f_type'] == 'M2M' and len(x['value']) > 0:
            for y in x['value']:
                graph['nodes'].append(as_node(y))
                graph['edges'].append(
                    {
                        'id': f"{as_node(instance)['id']}__{as_node(y)['id']}",
                        'source': as_node(instance)['id'],
                        'target': as_node(y)['id'],
                        'label': x['verbose_name']
                    }
                )
        elif x['f_type'] == 'REVRESE_RELATION' and len(x['value']) > 0:
            for y in x['value']:
                graph['nodes'].append(as_node(y))
                graph['edges'].append(
                    {
                        'id': f"{as_node(instance)['id']}__{as_node(y)['id']}",
                        'source': as_node(instance)['id'],
                        'target': as_node(y)['id'],
                        'label': x['verbose_name']
                    }
                )
    return graph
