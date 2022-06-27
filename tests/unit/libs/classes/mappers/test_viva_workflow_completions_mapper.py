from app.libs.classes.mappers.viva_workflow_completions_mapper import VivaWorkflowCompletionsMapper


viva_workflow = {
    'application': {
        'completionsreceived': None,
        'completions': {
            'completion': [
                'Hyreskontrakt',
                'Underlag på alla sökta utgifter',
                'Underlag på alla inkomster/tillgångar',
                'Alla kontoutdrag för hela förra månaden och fram till idag',
                'Kom in med...',
            ]
        },
        'completiondescription': 'Du behöver komplettera ansökan.',
    }
}

viva_workflow_completion_not_list = {
    'application': {
        'completionsreceived': None,
        'completions': {
            'completion': 'Kom in med...',
        },
        'completiondescription': None,
    }
}

viva_workflow_completionuploaded_list = {
    'application': {
        'completionsuploaded': {
            'completionuploaded': [
                'TEST1',
                'TEST2',
                'TEST3',
            ],
        },
    },
}

viva_workflow_completionuploaded_single = {
    'application': {
        'completionsuploaded': {
            'completionuploaded': 'TEST101',
        },
    },
}


def test_initial_completions():
    completion_mapper = VivaWorkflowCompletionsMapper(
        viva_workflow=viva_workflow)
    completion_list = completion_mapper.get_completion_list()

    assert completion_mapper.is_random_check is False
    assert completion_list == [
        {
            'description': 'Hyreskontrakt',
            'received': False,
        },
        {
            'description': 'Underlag på alla sökta utgifter',
            'received': False,
        },
        {
            'description': 'Underlag på alla inkomster/tillgångar',
            'received': False,
        },
        {
            'description': 'Alla kontoutdrag för hela förra månaden och fram till idag',
            'received': False,
        },
        {
            'description': 'Kom in med...',
            'received': False,
        },
    ]


def test_completion_list_partially_approved():
    viva_workflow['application']['completionsreceived'] = {
        'completionreceived': [
            'Hyreskontrakt',
            'Underlag på alla sökta utgifter'
        ]
    }

    completion_mapper = VivaWorkflowCompletionsMapper(viva_workflow)
    completion_list = completion_mapper.get_completion_list()

    assert completion_list == [
        {
            'description': 'Hyreskontrakt',
            'received': True,
        },
        {
            'description': 'Underlag på alla sökta utgifter',
            'received': True,
        },
        {
            'description': 'Underlag på alla inkomster/tillgångar',
            'received': False,
        },
        {
            'description': 'Alla kontoutdrag för hela förra månaden och fram till idag',
            'received': False,
        },
        {
            'description': 'Kom in med...',
            'received': False,
        },
    ]


def test_completion_list_all_received():
    viva_workflow['application']['completionsreceived'] = None
    viva_workflow['application']['completions'] = None

    completion_mapper = VivaWorkflowCompletionsMapper(viva_workflow)
    completion_list = completion_mapper.get_completion_list()

    assert completion_list == []


def test_completion_not_list():
    completion_mapper = VivaWorkflowCompletionsMapper(
        viva_workflow_completion_not_list)
    completion_list = completion_mapper.get_completion_list()

    assert completion_list == [
        {
            'description': 'Kom in med...',
            'received': False,
        },
    ]


def test_is_random_check():
    viva_workflow['application']['completiondescription'] = 'Du är utvald för stickprovskontroll.'
    completion_mapper = VivaWorkflowCompletionsMapper(viva_workflow)

    assert completion_mapper.is_random_check is True


def test_is_random_check_none():
    viva_workflow['application']['completiondescription'] = None

    completion_mapper = VivaWorkflowCompletionsMapper(viva_workflow)

    assert completion_mapper.is_random_check is False


def test_is_due_date_expired():
    viva_workflow['application']['completionduedate'] = '2022-05-01'
    completion_mapper = VivaWorkflowCompletionsMapper(viva_workflow)

    assert completion_mapper.is_due_date_expired is True


def test_is_not_due_date_expired():
    viva_workflow['application']['completionduedate'] = '2100-05-10'
    completion_mapper = VivaWorkflowCompletionsMapper(viva_workflow)

    assert completion_mapper.is_due_date_expired is False


def test_received_date():
    viva_workflow['application']['completionreceiveddate'] = '2022-05-01'
    completion_mapper = VivaWorkflowCompletionsMapper(viva_workflow)

    assert completion_mapper.received_date == 1651356000000


def test_completions_uploaded():
    completion_mapper = VivaWorkflowCompletionsMapper(
        viva_workflow_completionuploaded_list)

    completion_uploaded = completion_mapper.get_completion_uploaded()

    assert completion_uploaded == ['TEST1', 'TEST2', 'TEST3']


def test_completions_single_uploaded():
    completion_mapper = VivaWorkflowCompletionsMapper(
        viva_workflow_completionuploaded_single)

    completion_uploaded = completion_mapper.get_completion_uploaded()

    assert completion_uploaded == ['TEST101']


def test_completions_none_uploaded():
    viva_workflow_completionuploaded_none = {
        'application': {
            'completionsuploaded': None,
        },
    }

    completion_mapper = VivaWorkflowCompletionsMapper(
        viva_workflow_completionuploaded_none)

    completion_uploaded = completion_mapper.get_completion_uploaded()

    assert completion_uploaded == []


def test_completions_description():
    viva_workflow['application']['completiondescription'] = 'Du behöver komplettera ansökan.'
    completion_mapper = VivaWorkflowCompletionsMapper(viva_workflow=viva_workflow)

    assert completion_mapper.description == 'Du behöver komplettera ansökan.'
