from .TokenSpan import TokenSpan
from .remove_list_duplicates import remove_list_duplicates
from .EntityType import EntityType

class Entity(TokenSpan):

	def __init__(self, obj, document):
		super().__init__(obj=obj, document=document)
		for token in self.tokens:
			token._entity = self

	@property
	def name(self):
		return self._obj

	@property
	def parent_noun_chunks(self):
		return [nc for nc in self.document.noun_chunks if nc.start <= self.start and nc.end >= self.end]

	@property
	def child_noun_chunks(self):
		return [nc for nc in self.document.noun_chunks if nc.start >= self.start and nc.end <= self.end]

	@property
	def noun_chunks(self):
		return remove_list_duplicates(self.parent_noun_chunks + self.child_noun_chunks)


	@property
	def id(self):
		return (self.document.id, 'entity', self.start, self.end)

	def graph_str(self):
		return f"{self}\n({str(self.entity_type).replace('_', ' ')})"

	@property
	def entity_type(self):
		"""
		:rtype: EntityType
		"""
		return self.tokens[0].entity_type