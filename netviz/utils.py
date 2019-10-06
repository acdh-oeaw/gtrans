import random

from django.contrib.contenttypes.models import ContentType

from browsing.browsing_utils import model_to_dict


def color_generator(number_of_colors=5):
    """ generats some random Hex Color Codes
        taken from https://stackoverflow.com/questions/28999287/generate-random-colors-rgb
        :param number_of_colors: The number colors to generate
        :return: A list of Hex COlor Codes
    """

    number_of_colors = number_of_colors
    color = [
        "#"+''.join(
            [random.choice('0123456789ABCDEF') for j in range(6)]
        ) for i in range(number_of_colors)
    ]
    return color


def as_node(instance):
    """ serializes an object as netvis-nodes
        :param instance: An instance of a django model class
        :return: A dict with keys 'type', 'label' and 'id'
    """
    node = {}
    node["type"] = f"{instance._meta.app_label}__{instance.__class__.__name__}"
    node["label"] = f"{instance.__str__()}"
    node["id"] = f"{node['type'].lower()}__{instance.id}"
    return node


def add_node_types(base_graph):
    """ takes a base graph (nodes and edges) and adds node and edge type arrays
        :param base_grape: A dict with node and edges arrays
        :return: A dict according to netvis graph data model
    """
    graph = base_graph
    graph['types'] = {
        'nodes': [],
        'edges': []
    }
    nodes = [x['type'] for x in graph['nodes']]
    colors_dict = dict(zip(set(nodes), color_generator(len(set(nodes)))))
    for x in set(nodes):
        app_label, model = x.split('__')[:2]
        ct = ContentType.objects.get(
            app_label=app_label, model=model
        ).model_class()._meta.verbose_name
        graph['types']['nodes'].append(
            {
                'id': x,
                'label': ct,
                'color': colors_dict[x]
            }
        )
    return graph


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
    new_graph = add_node_types(graph)
    return new_graph
