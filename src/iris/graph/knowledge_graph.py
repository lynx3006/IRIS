import networkx as nx

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.MultiDiGraph()

    def add_entity(
        self,
        entity_id: str,
        entity_type: str,
        **attributes,
    ):
        self.graph.add_node(
            entity_id,
            entity_type=entity_type,
            **attributes,
        )

    def add_relation(
        self,
        source_id: str,
        target_id: str,
        relation: str,
        **attributes,
    ):
        if source_id not in self.graph:
            raise ValueError(f"Unknown source entity: {source_id}")

        if target_id not in self.graph:
            raise ValueError(f"Unknown target entity: {target_id}")

        self.graph.add_edge(
            source_id,
            target_id,
            relation=relation,
            **attributes,
        )

    def get_entity(self, entity_id: str):
        if entity_id not in self.graph:
            return None

        return self.graph.nodes[entity_id]

    def get_relations(self, entity_id: str):
        if entity_id not in self.graph:
            return []

        relations = []

        for source, target, data in self.graph.edges(
            entity_id, data=True
        ):
            relations.append({
                "source": source,
                "target": target,
                **data,
            })

        for source, target, data in self.graph.in_edges(
            entity_id, data=True
        ):
            relations.append({
                "source": source,
                "target": target,
                **data,
            })

        return relations