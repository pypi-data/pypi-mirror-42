from typing import List, Optional, Any

from cortex_profiles.schemas.schemas import CONTEXTS
from cortex_profiles.synthetic.base import BaseProviderWithDependencies
from cortex_profiles.synthetic.tenant import TenantProvider
from cortex_profiles.types.attribute_values import \
    Dimension, ObjectAttributeValue, RelationshipAttributeValue, NumericAttributeValue, PercentileAttributeValue \
    , PercentageAttributeValue, AverageAttributeValue, CounterAttributeValue, TotalAttributeValue, \
    DimensionalAttributeValue, StringAttributeValue, DecimalAttributeValue, IntegerAttributeValue, BooleanAttributeValue, PrimitiveAttributeValue, ListAttributeValue, ConceptAttributeValue, WeightedAttributeValue
from cortex_profiles.utils import unique_id

# Add this to the configurable universe ...
PROFILE_TYPES = [
    "cortex/end-user-profile",
    "cortex/investor-profile",
    "cortex/medical-client-profile",
    "cortex/shopper-profile"
]

class AttributeValueProvider(BaseProviderWithDependencies):

    # def __init__(self, *args, **kwargs):
    #     super(AttributeValueProvider, self).__init__(*args, **kwargs)
    #     self.fake = args[0]

    def dependencies(self) -> List[type]:
        return [
            TenantProvider
        ]

    def dimensional_value(self, max_dimensions=7) -> DimensionalAttributeValue:
        dimensions = [
            Dimension(dimensionId=unique_id(), dimensionValue=self.fake.random.randint(0, 100))
            for x in self.fake.range(0, max_dimensions)
        ]
        return DimensionalAttributeValue(
            value=dimensions,
            contextOfDimension = self.fake.random.choice(list(CONTEXTS.keys())),
            contextOfDimensionValue = "int"   # What type is the value associated with the dimension?
        )

    def string_value(self) -> StringAttributeValue:
        return StringAttributeValue(value=self.fake.color_name())

    def integer_value(self) -> IntegerAttributeValue:
        return IntegerAttributeValue(value=self.fake.random.randint(0, 100))

    def decimal_value(self) -> DecimalAttributeValue:
        return DecimalAttributeValue(value=self.fake.random.randint(0, 100) / 0.1)

    def boolean_value(self) -> BooleanAttributeValue:
        return BooleanAttributeValue(value=self.fake.random.choice([True, False]))

    def object_value(self) -> ObjectAttributeValue:
        return ObjectAttributeValue(value=dict(zip(["favorite_color"], [self.fake.color_name()])))

    def list_value(self) -> ListAttributeValue:
        return ListAttributeValue(value=self.fake.random_subset_of_list(list(
            set(list(map(lambda x: x(), [self.fake.color_name]*10)))
        )))

    def primitive_value(self) -> PrimitiveAttributeValue:
        return PrimitiveAttributeValue(
            value=self.fake.random.choice([
                self.string_value,
                self.boolean_value,
                self.integer_value,
                self.decimal_value,
            ])().value
        )

    def percentile_value(self) -> PercentileAttributeValue:
        return PercentileAttributeValue(value=min(self.fake.random.randint(0, 100) * 0.98, 100))

    def percentage_value(self) -> PercentageAttributeValue:
        return PercentageAttributeValue(value=min(self.fake.random.randint(0, 100) * 0.98, 100))

    def average_value(self) -> AverageAttributeValue:
        return AverageAttributeValue(value=self.fake.random.randint(0, 1000) * 0.98)

    def numeric_value(self) -> NumericAttributeValue:
        return NumericAttributeValue(value=self.fake.random.choice([int, float])(self.fake.random.randint(0,100) * 0.123))

    def counter_value(self) -> CounterAttributeValue:
        return CounterAttributeValue(value=self.fake.random.randint(0, 2500))

    def total_value(self) -> TotalAttributeValue:
        return TotalAttributeValue(value=self.numeric_value().value)

    def relationship_value(self) -> RelationshipAttributeValue:
        return RelationshipAttributeValue(
            value=unique_id(),
            relatedConceptType=self.fake.random.choice(list(CONTEXTS.keys())),
            relationshipType="cortex/likes",
            relationshipTitle="Likes",
            relatedConceptTitle=self.fake.company(),
            relationshipProperties={}
        )

    def concept_value(self) -> ConceptAttributeValue:
        return ConceptAttributeValue(
            value=unique_id()
        )

    def weighted_value(self, value:Optional[Any]=None) -> WeightedAttributeValue:
        return WeightedAttributeValue(
            value=value if value is not None else self.fake.company(),
            weight=self.fake.random.randint(0,100) / 100.00
        )

    def profile_type_value(self) -> ListAttributeValue:
        return ListAttributeValue(
            value=self.fake.random_subset_of_list([
                PROFILE_TYPES
            ])
        )

    def attribute_value(self):
        return self.fake.random.choice([
            self.dimensional_value,
            self.object_value,
            self.relationship_value,
            self.numeric_value,
            self.percentage_value,
            self.percentile_value,
            self.average_value,
            self.counter_value,
            self.total_value,
            self.profile_type_value
        ])()


def test_attr_value_provider(f):
    # print(f.attributes_for_single_profile())
    for x in range(0, 100):
        print(f.attribute_value())


if __name__ == "__main__":
    import json, attr
    from cortex_profiles.synthetic import create_profile_synthesizer
    import os
    import inspect

    def get_var_names(var):
        callers_local_vars = inspect.currentframe().f_back.f_locals.items()
        return [k for k, v in callers_local_vars if v is var]

    synth = create_profile_synthesizer()

    # test_attr_value_provider(synth)

    string_value = synth.string_value()
    integer_value = synth.integer_value()
    decimal_value = synth.decimal_value()
    boolean_value = synth.boolean_value()
    object_value = synth.object_value()
    list_value = synth.list_value()
    primitive_value = synth.primitive_value()
    percentile_value = synth.percentile_value()
    percentage_value = synth.percentage_value()
    average_value = synth.average_value()
    numeric_value = synth.numeric_value()
    counter_value = synth.counter_value()
    total_value = synth.total_value()
    relationship_value = synth.relationship_value()
    concept_value = synth.concept_value()
    weighted_value = synth.weighted_value()

    filepath = "{}/../../samples/good-attribute-values.js".format(os.path.dirname(__file__))
    # filepath = os.path.expanduser("~/Workspace/git/cortex-graph/test/attribute-value-samples/attribute-values.js")
    with open(filepath, "w") as fh:
        fh.write("const GoodAttributeValues = ")
        json.dump({
            string_value.context: attr.asdict(string_value),
            integer_value.context: attr.asdict(integer_value),
            decimal_value.context: attr.asdict(decimal_value),
            boolean_value.context: attr.asdict(boolean_value),
            object_value.context: attr.asdict(object_value),
            list_value.context: attr.asdict(list_value),
            primitive_value.context: attr.asdict(primitive_value),
            percentile_value.context: attr.asdict(percentile_value),
            percentage_value.context: attr.asdict(percentage_value),
            average_value.context: attr.asdict(average_value),
            numeric_value.context: attr.asdict(numeric_value),
            counter_value.context: attr.asdict(counter_value),
            total_value.context: attr.asdict(total_value),
            relationship_value.context: attr.asdict(relationship_value),
            concept_value.context: attr.asdict(concept_value),
            weighted_value.context: attr.asdict(weighted_value),
        }, fh, indent=4)
        fh.write(";\n")
        fh.write("module.exports = { GoodAttributeValues } ;")

    for x in [string_value, integer_value, decimal_value, boolean_value, object_value, list_value, primitive_value,
              percentile_value, percentage_value, average_value, numeric_value, counter_value, total_value,
              relationship_value, concept_value, weighted_value]:
        with open("{}/../../samples/attribute_values/{}.json".format(os.path.dirname(__file__), get_var_names(x)[0]), "w") as fh:
            json.dump(attr.asdict(x), fh, indent=4)