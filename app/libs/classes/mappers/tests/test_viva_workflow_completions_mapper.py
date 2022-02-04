from ..viva_workflow_completions_mapper import VivaWorkflowCompletionsMapper


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


def test_initial_completions():
    completion_mapper = VivaWorkflowCompletionsMapper(viva_workflow)
    completion_list = completion_mapper.get_completion_list()
    random_check = completion_mapper.is_random_check()

    assert random_check is False
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


def test_is_random_check():
    viva_workflow['application']['completiondescription'] = 'Du är utvald för stickprovskontroll.'

    completion_mapper = VivaWorkflowCompletionsMapper(viva_workflow)
    random_check = completion_mapper.is_random_check()

    assert random_check is True


def test_is_random_check_none():
    viva_workflow['application']['completiondescription'] = None

    completion_mapper = VivaWorkflowCompletionsMapper(viva_workflow)
    random_check = completion_mapper.is_random_check()

    assert random_check is False


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


def test_empty_completion_description():
    completion_mapper = VivaWorkflowCompletionsMapper(
        viva_workflow_completion_not_list)

    completion_list = completion_mapper.get_completion_list()

    assert completion_list == [
        {
            'description': 'Kom in med...',
            'received': False,
        },
    ]
