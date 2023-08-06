# Welcome to pyBIS!
pyBIS is a Python module for interacting with openBIS, designed to be used in Jupyter. It offers a sort of IDE for openBIS, supporting TAB completition and input checks, making the life of a researcher hopefully easier.



# SYNOPSIS

## connecting to OpenBIS
```
from pybis import Openbis
o = Openbis('https://example.com:8443', verify_certificates=False)
o.login('username', 'password', save_token=True)   # saves the session token in ~/.pybis/example.com.token
o.token
o.is_session_active()
o.get_datastores()
o.logout()
```

## Masterdata
```
o.get_experiment_types()
et = o.get_experiment_type('TEST')
et.get_propertyAssignments()

o.get_sample_types()
st = o.get_sample_type('YEAST')
et.get_propertyAssignments()

o.get_material_types()
mt = o.get_material_type('GENE')
mt.get_propertyAssignments()

o.get_dataset_types()
dst = o.get_dataset_types()[0]
dst = o.get_dataset_type('RAW_DATA')
dst.get_propertyAssignments()

o.get_vocabularies()
o.get_vocabulary('BACTERIAL_ANTIBIOTIC_RESISTANCE')
o.get_terms(vocabulary='STORAGE')
o.get_tags()
```

## Users, Groups and RoleAssignments

```
o.get_groups()
group = o.new_group(code='group_name', description='...')
group = o.get_group('group_name')
group.save()
group.assign_role(role='ADMIN', space='DEFAULT')
group.get_roles() 
group.revoke_role(role='ADMIN', space='DEFAULT')

group.add_persons(['admin'])
group.get_persons()
group.del_persons(['admin'])
group.delete()

o.get_persons()
person = o.new_person(userId='username')
person.space = 'USER_SPACE'
person.save()

person.assign_role(role='ADMIN', space='MY_SPACE')
person.assign_role(role='OBSERVER')
person.get_roles()
person.revoke_role(role='ADMIN', space='MY_SPACE')
person.revoke_role(role='OBSERVER')

o.get_role_assignments()
o.get_role_assignments(space='MY_SPACE')
o.get_role_assignments(group='MY_GROUP')
ra = o.get_role_assignment(techId)
ra.delete()
```


## Spaces
```
space = o.new_space(code='space_name', description='')
space.save()
space.delete('reason for deletion')
o.get_spaces()
o.get_space('MY_SPACE')
```

## Projects
```
project = o.new_project(
    space=space, 
    code='project_name',
    description='some project description'
)
project = space.new_project( code='project_code', description='project description')
project.save()

o.get_projects()
o.get_projects(space='MY_SPACE')
space.get_projects()

project.get_experiments()
project.get_attachments()
p.add_attachment(fileName='testfile', description= 'another file', title= 'one more attachment')
project.download_attachments()
```

## Samples
Samples are nowadays called **Objects** in openBIS. pyBIS is not yet thoroughly supporting this term in all methods where «sample» occurs.

```
sample = o.new_sample(
    type     = 'YEAST', 
    space    = 'MY_SPACE', 
    parents  = [parent_sample, '/MY_SPACE/YEA66'], 
    children = [child_sample],
    props    = {"name": "some name", "description": "something interesting"}
)
sample = space.new_sample( type='YEAST' )
sample.save()

sample = o.get_sample('/MY_SPACE/MY_SAMPLE_CODE')
sample = o.get_sample('20170518112808649-52')

sample.space
sample.code
sample.permId
sample.identifier
sample.type  # once the sample type is defined, you cannot modify it

sample.space
sample.space = 'MY_OTHER_SPACE'

sample.experiment    # a sample can belong to one experiment only
sample.experiment = '/MY_SPACE/MY_PROJECT/MY_EXPERIMENT'

sample.project
sample.project = '/MY_SPACE/MY_PROJECT'  # only works if project samples are
enabled

sample.tags
sample.tags = ['guten_tag', 'zahl_tag' ]

sample.get_parents()
sample.set_parents(['/MY_SPACE/PARENT_SAMPLE_NAME')
sample.add_parents('/MY_SPACE/PARENT_SAMPLE_NAME')
sample.del_parents('/MY_SPACE/PARENT_SAMPLE_NAME')

sample.get_children()
sample.set_children('/MY_SPACE/CHILD_SAMPLE_NAME')
sample.add_children('/MY_SPACE/CHILD_SAMPLE_NAME')
sample.del_children('/MY_SPACE/CHILD_SAMPLE_NAME')

# A Sample may belong to another Sample, which acts as a container.
# As opposed to DataSets, a Sample may only belong to one container.
sample.container    # returns a sample object
sample.container = '/MY_SPACE/CONTAINER_SAMPLE_NAME'   # watch out, this will change the identifier of the sample to:
                                                       # /MY_SPACE/CONTAINER_SAMPLE_NAME:SAMPLE_NAME
sample.container = ''                                  # this will remove the container. 

# A Sample may contain other Samples, in order to act like a container (see above)
# The Sample-objects inside that Sample are called «components» or «contained Samples»
# You may also use the xxx_contained() functions, which are just aliases.
sample.get_components()
sample.set_components('/MY_SPACE/COMPONENT_NAME')
sample.add_components('/MY_SPACE/COMPONENT_NAME')
sample.del_components('/MY_SPACE/COMPONENT_NAME')

sample.get_tags()
sample.set_tags('tag1')
sample.add_tags(['tag2','tag3'])
sample.del_tags('tag1')

sample.set_props({ ... })
sample.p                              # same thing as .props
sample.p.my_property = "some value"   # set the value of a property (value is checked)
sample.p + TAB                        # in IPython or Jupyter: show list of available properties
sample.p.my_property_ + TAB           # in IPython or Jupyter: show datatype or controlled vocabulary

sample.get_attachments()
sample.download_attachments()
sample.add_attachment('testfile.xls')

samples = o.get_samples(
    space ='MY_SPACE',
    type  ='YEAST',
    tags  =['*'],                     # only sample with existing tags
    NAME  = 'some name',              # properties are always uppercase 
                                      # to distinguish them from attributes
    **{ "SOME.WEIRD:PROP": "value"}   # property name contains a dot or a
                                      # colon: cannot be passed as an argument 
    props=['NAME', 'MATING_TYPE']     # show these properties in the result
)
samples.df                            # returns a pandas dataframe object
samples.get_datasets(type='ANALYZED_DATA')
```


## Experiments

```
o.new_experiment
    type='DEFAULT_EXPERIMENT',
    space='MY_SPACE',
    project='YEASTS'
)
o.get_experiments(
    project='YEASTS',
    space='MY_SPACE', 
    type='DEFAULT_EXPERIMENT',
    tags='*', 
    finished_flag=False,
    props=['name', 'finished_flag']
)
exp = o.get_experiment('/MY_SPACE/MY_PROJECT/MY_EXPERIMENT')

exp.props
exp.p                              # same thing as .props
exp.p.finished_flag=True
exp.p.my_property = "some value"   # set the value of a property (value is checked)
exp.p + TAB                        # in IPython or Jupyter: show list of available properties
exp.p.my_property_ + TAB           # in IPython or Jupyter: show datatype or controlled vocabulary

exp.attrs
exp.a     # same as exp.attrs
exp.attrs.tags = ['some', 'extra', 'tags']
exp.tags = ['some', 'extra', 'tags']          # same thing
exp.save()
```

## Datasets

```
sample.get_datasets()
ds = o.get_dataset('20160719143426517-259')
ds.get_parents()
ds.get_children()
ds.sample
ds.experiment
ds.physicalData
ds.status              # AVAILABLE LOCKED ARCHIVED 
                       # UNARCHIVE_PENDING ARCHIVE_PENDING BACKUP_PENDING
ds.archive()
ds.unarchive()

ds.get_files(start_folder="/")
ds.file_list
ds.add_attachment()
ds.get_attachments()
ds.download_attachments()
ds.download(destination='/tmp', wait_until_finished=False)

ds_new = o.new_dataset(
    type       = 'ANALYZED_DATA', 
    experiment = '/SPACE/PROJECT/EXP1', 
    sample     = '/SPACE/SAMP1',
    files      = ['my_analyzed_data.dat'], 
    props      = {'name': 'some good name', 'description': '...' })
)

# DataSet CONTAINER (contains other DataSets, but no files)
ds_new = o.new_dataset(
    type       = 'ANALYZED_DATA', 
    experiment = '/SPACE/PROJECT/EXP1', 
    sample     = '/SPACE/SAMP1',
    kind       = 'CONTAINER',
    props      = {'name': 'some good name', 'description': '...' })
)

ds_new.save()

dataset.get_parents()
dataset.set_parents(['20170115220259155-412'])
dataset.add_parents(['20170115220259155-412'])
dataset.del_parents(['20170115220259155-412'])

dataset.get_children()
dataset.set_children(['20170115220259155-412'])
dataset.add_children(['20170115220259155-412'])
dataset.del_children(['20170115220259155-412'])

# A DataSet may belong to other DataSets, which must be of kind=CONTAINER
# As opposed to Samples, DataSets may belong (contained) to more than one DataSet-container
dataset.get_containers()
dataset.set_containers(['20170115220259155-412'])
dataset.add_containers(['20170115220259155-412'])
dataset.del_containers(['20170115220259155-412'])

# A DataSet of kind=CONTAINER may contain other DataSets, to act like a folder (see above)
# The DataSet-objects inside that DataSet are called components or contained DataSets
# You may also use the xxx_contained() functions, which are just aliases.
dataset.get_components()
dataset.set_components(['20170115220259155-412'])
dataset.add_components(['20170115220259155-412'])
dataset.del_components(['20170115220259155-412'])

ds.set_properties({...})
ds.props
ds.p                              # same thing as .props
ds.p.my_property = "some value"   # set the value of a property
ds.p + TAB                        # show list of available properties
ds.p.my_property_ + TAB           # show datatype or controlled vocabulary

# complex query with chaining.
# properties must be in UPPERCASE
datasets = o.get_experiments(project='YEASTS').get_samples(type='FLY').get_datasets(type='ANALYZED_DATA', props=['MY_PROPERTY'],MY_PROPERTY='some analyzed data')

# another example
datasets = o.get_experiment('/MY_NEW_SPACE/VERMEUL_PROJECT/MY_EXPERIMENT4').get_samples(type='UNKNOWN').get_parents().get_datasets(type='RAW_DATA')

datasets.df                       # get a pandas dataFrame object

# use it in a for-loop:
for dataset in datasets:
    print(ds.permID)
```

## Semantic Annotations
```
# create semantic annotation for sample type 'UNKNOWN'
sa = o.new_semantic_annotation(
	entityType = 'UNKNOWN',
	predicateOntologyId = 'po_id',
	predicateOntologyVersion = 'po_version',
	predicateAccessionId = 'pa_id',
	descriptorOntologyId = 'do_id',
	descriptorOntologyVersion = 'do_version',
	descriptorAccessionId = 'da_id'
)
sa.save()

# create semantic annotation for property type 
# (predicate and descriptor values omitted for brevity)
sa = o.new_semantic_annotation(propertyType = 'DESCRIPTION', ...)
sa.save()

# create semantic annotation for sample property assignment (predicate and descriptor values omitted for brevity)
sa = o.new_semantic_annotation(entityType = 'UNKNOWN', propertyType = 'DESCRIPTION', ...)
sa.save()

# create a semantic annotation directly from a sample type
# will also create sample property assignment annotations when propertyType is given
st = o.get_sample_type("ORDER")
st.new_semantic_annotation(...)

# get all semantic annotations
o.get_semantic_annotations()

# get semantic annotation by perm id
sa = o.get_semantic_annotation("20171015135637955-30")

# update semantic annotation
sa.predicateOntologyId = 'new_po_id'
sa.descriptorOntologyId = 'new_do_id'
sa.save()

# delete semantic annotation
sa.delete('reason')
```

## Tags
```
new_tag = o.new_tag(
	code        = 'my_tag', 
	description = 'some descriptive text'
)
new_tag.description = 'some new description'
new_tag.save()
o.get_tags()
o.get_tag('/username/TAG_Name')
o.get_tag('TAG_Name')

tag.get_experiments()
tag.get_samples()
tag.delete()
```

## Vocabualry and VocabularyTerms

An entity such as Sample (Object), Experiment (Collection), Material or DataSet can be of a specific type:

* Sample Type
* Experiment Type
* DataSet Type
* Material Type

Every type defines which Properties may be defined. Properties are like Attributes, but they are Type specific. Properties can contain all sorts of information, such as free text, XML, Hyperlink, Boolean and also *Controlled Vocabulary*. Such a Controlled Vocabulary consists of many VocabularyTerms. They are used to check the terms entered in a Property field.

So for example, you want to add a property called **Animal** to a Sample and you want to control which terms are entered in this Property field. For this you need to do a couple of steps:

1. create a new vocabulary *AnimalVocabulary*
2. add terms to that vocabulary: *Cat, Dog, Mouse*
3. create a new PropertyType (e.g. *Animal*) of DataType *CONTROLLEDVOCABULARY* and assign the *AnimalVocabulary* to it
4. create a new SampleType (e.g. *Pet*) and *assign* the created PropertyType to that Sample type.
5. If you now create a new Sample of type *Pet* you will be able to add a property *Animal* to it which only accepts the terms *Cat, Dog* or *Mouse*.


**create new Vocabulary with three VocabularyTerms**

```
voc = o.new_vocabulary(
    code = 'BBB',
    description = 'description of vocabulary aaa',
    urlTemplate = 'https://ethz.ch',
    terms = [
        { "code": 'term_code1', "label": "term_label1", "description": "term_description1"},
        { "code": 'term_code2', "label": "term_label2", "description": "term_description2"},
        { "code": 'term_code3', "label": "term_label3", "description": "term_description3"}
    ]   
)
voc.save()
```

**create additional VocabularyTerms**

```
term = o.new_term(
	code='TERM_CODE_XXX', 
	vocabularyCode='BBB', 
	label='here comes a label',
	description='here is a meandingful description'
)
term.save()
```

**fetching Vocabulary and VocabularyTerms**




# Requirements and organization

### Dependencies and Requirements
- pyBIS relies the openBIS API v3; openBIS version 16.05.2 or newer 
- pyBIS uses Python 3.3 and pandas
- pyBIS needs the jupyter-api to be installed, in order to register new datasets

### Installation

- locate the `jupyter-api` folder found in `pybis/src/coreplugins`
- copy this folder to `openbis/servers/core-plugins` in your openBIS installation
- register the plugin by editing `openbis/servers/core-plugins/core-plugins.properties` :
- `enabled-modules = jupyter-api` (separate multiple plugins with comma)
- restart your DSS to activate the plugin


### Project Organization
This project is devided in several parts:

- src/python/**PyBis** Python module which holds all the method to interact with OpenBIS
- src/python/**OBis** a command-line tool to register large datasets in OpenBIS without actually copying the data. Uses git annex for version control and OpenBIS linkedDataSet objects to register the metadata.
- src/python/**JupyterBis** a JupyterHub authenticator module which uses pyBIS for authenticating against openBIS, validating and storing the session token
- src/core-plugins/**jupyter-api**, an ingestion plug-in for openBIS, allowing people to upload new datasets
- src/vagrant/**jupyter-bis/Vagrantfile** to set up JupyterHub on a virtual machine (CentOS 7), which uses the JupyterBis authenticator module
- src/vagrant/**obis/Vagrantfile** to set up a complete OpenBIS instance on a virtual machine (CentOS 7)
- 
