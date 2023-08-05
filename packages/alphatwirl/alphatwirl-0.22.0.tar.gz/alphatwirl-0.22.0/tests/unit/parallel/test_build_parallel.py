# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import sys

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

has_jupyter_notebook = False
try:
    from alphatwirl.progressbar import ProgressBarJupyter
    has_jupyter_notebook = True
except ImportError:
    pass

from alphatwirl.parallel import build_parallel
from alphatwirl.parallel.build import build_parallel_multiprocessing

##__________________________________________________________________||
@pytest.fixture(
    params=[True, False]
)
def isatty(request, monkeypatch):
    ret = request.param
    org_stdout = sys.stdout
    f = mock.Mock(**{
        'stdout.isatty.return_value': ret,
        'stdout.write.side_effect': lambda x : org_stdout.write(x)
    })
    module = sys.modules['alphatwirl.parallel.build']
    monkeypatch.setattr(module, 'sys', f)
    return ret

##__________________________________________________________________||
if has_jupyter_notebook:
    is_jupyter_notebook_parames = [True, False]
else:
    is_jupyter_notebook_parames = [False]

@pytest.fixture(params=is_jupyter_notebook_parames)
def is_jupyter_notebook(request, monkeypatch):
    ret = request.param
    f = mock.Mock()
    f.return_value = ret
    module = sys.modules['alphatwirl.parallel.build']
    monkeypatch.setattr(module, 'is_jupyter_notebook', f)
    return ret

##__________________________________________________________________||
@pytest.mark.parametrize('processes', [0, 1, 3])
@pytest.mark.parametrize('quiet', [True, False])
def test_build_parallel_multiprocessing(quiet, processes):

    parallel_mode = 'multiprocessing'
    parallel = build_parallel(
        parallel_mode=parallel_mode,
        quiet=quiet,
        processes=processes,
    )

    ## communicationChannel
    if processes == 0:
        assert 'CommunicationChannel0' == parallel.communicationChannel.__class__.__name__
    else:
        assert 'CommunicationChannel' == parallel.communicationChannel.__class__.__name__
        assert 'MultiprocessingDropbox' ==  parallel.communicationChannel.dropbox.__class__.__name__
        assert quiet == (not parallel.communicationChannel.dropbox.progressbar)

    ## workingarea
    assert parallel.workingarea is None

##__________________________________________________________________||
def test_build_logging_unknown_parallel_mode(caplog):

    with caplog.at_level(logging.WARNING):
        parallel = build_parallel(parallel_mode='unknown_mode')

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'parallel.build' in caplog.records[0].name
    assert 'unknown parallel_mode' in caplog.records[0].msg

    assert 'MultiprocessingDropbox' ==  parallel.communicationChannel.dropbox.__class__.__name__

##__________________________________________________________________||
@pytest.mark.parametrize('dispatcher_options', [dict()])
@pytest.mark.parametrize('user_modules', [[], ['scribblers']])
def test_build_parallel_subprocess(user_modules, dispatcher_options):

    parallel_mode = 'subprocess'

    parallel = build_parallel(
        parallel_mode=parallel_mode,
        user_modules=user_modules,
        dispatcher_options=dispatcher_options
    )

    ## communicationChannel
    assert 'CommunicationChannel' == parallel.communicationChannel.__class__.__name__
    assert 'TaskPackageDropbox' == parallel.communicationChannel.dropbox.__class__.__name__

    ## dispatcher
    assert 'SubprocessRunner' == parallel.communicationChannel.dropbox.dispatcher.__class__.__name__

    assert 'WorkingArea' == parallel.workingarea.__class__.__name__

    if user_modules:
        assert set(['scribblers', 'alphatwirl']) == set(parallel.workingarea.python_modules)
    else:
        assert set(['alphatwirl']) == set(parallel.workingarea.python_modules)


@pytest.mark.parametrize('dispatcher_options', [dict(), dict(job_desc_dict=dict(request_memory='120'))])
@pytest.mark.parametrize('htcondor_job_desc_extra', [[], ['request_memory = 250']])
@pytest.mark.parametrize('user_modules', [[], ['scribblers']])
def test_build_parallel_htcondor(
        user_modules, htcondor_job_desc_extra,
        dispatcher_options):

    parallel_mode = 'htcondor'

    parallel = build_parallel(
        parallel_mode=parallel_mode,
        user_modules=user_modules,
        htcondor_job_desc_extra=htcondor_job_desc_extra,
        dispatcher_options=dispatcher_options
    )

    ## communicationChannel
    assert 'CommunicationChannel' == parallel.communicationChannel.__class__.__name__
    assert 'TaskPackageDropbox' == parallel.communicationChannel.dropbox.__class__.__name__

    ## dispatcher
    assert 'HTCondorJobSubmitter' == parallel.communicationChannel.dropbox.dispatcher.__class__.__name__
    assert htcondor_job_desc_extra == parallel.communicationChannel.dropbox.dispatcher.job_desc_extra
    if 'job_desc_dict' in dispatcher_options:
        assert dispatcher_options['job_desc_dict'] == parallel.communicationChannel.dropbox.dispatcher.user_job_desc_dict

    assert 'WorkingArea' == parallel.workingarea.__class__.__name__

    if user_modules:
        assert set(['scribblers', 'alphatwirl']) == set(parallel.workingarea.python_modules)
    else:
        assert set(['alphatwirl']) == set(parallel.workingarea.python_modules)


##__________________________________________________________________||

##__________________________________________________________________||
def test_build_depricated(caplog):
    with caplog.at_level(logging.WARNING):
        parallel = build_parallel_multiprocessing(quiet=True, processes=4)

    communicationChannel = parallel.communicationChannel
    assert 'CommunicationChannel' == communicationChannel.__class__.__name__
    assert 'MultiprocessingDropbox' == communicationChannel.dropbox.__class__.__name__

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'parallel.build' in caplog.records[0].name
    assert 'deprecated' in caplog.records[0].msg

##__________________________________________________________________||
