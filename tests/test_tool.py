from unittest import TestCase
from unittest.mock import Mock, patch, call
from calrissian.tool import CalrissianCommandLineTool, calrissian_make_tool, CalrissianToolException
from calrissian.context import CalrissianLoadingContext


class CalrissianMakeToolTestCase(TestCase):

    @patch('calrissian.tool.CalrissianCommandLineTool')
    def test_make_tool_clt(self, mock_calrissian_clt):
        spec = {'class': 'CommandLineTool'}
        loadingContext = CalrissianLoadingContext()
        made_tool = calrissian_make_tool(spec, loadingContext)
        self.assertEqual(made_tool, mock_calrissian_clt.return_value)
        self.assertEqual(mock_calrissian_clt.call_args, call(spec, loadingContext))

    @patch('calrissian.tool.default_make_tool')
    def test_make_tool_default_make_tool(self, mock_default_make_tool):
        spec = {'class': 'AnyOtherThing'}
        loadingContext = Mock()
        made_tool = calrissian_make_tool(spec, loadingContext)
        self.assertEqual(made_tool, mock_default_make_tool.return_value)
        self.assertEqual(mock_default_make_tool.call_args, call(spec, loadingContext))


class CalrissianCommandLineToolTestCase(TestCase):

    def setUp(self):
        self.toolpath_object = {'id': '1', 'inputs': [], 'outputs': []}
        self.loadingContext = CalrissianLoadingContext()

    @patch('calrissian.tool.CalrissianCommandLineJob')
    def test_make_job_runner(self, mock_command_line_job):
        tool = CalrissianCommandLineTool(self.toolpath_object, self.loadingContext)
        runner = tool.make_job_runner(Mock())
        self.assertEqual(runner, mock_command_line_job)

    def test_fails_use_container_false(self):
        tool = CalrissianCommandLineTool(self.toolpath_object, self.loadingContext)
        runtimeContext = Mock(use_container=False)
        with self.assertRaises(CalrissianToolException) as context:
            tool.make_job_runner(runtimeContext)
        self.assertIn('use_container is disabled', str(context.exception))

    def test_fails_no_default_container(self):
        tool = CalrissianCommandLineTool(self.toolpath_object, self.loadingContext)
        runtimeContext = Mock()
        runtimeContext.find_default_container.return_value = None
        with self.assertRaises(CalrissianToolException) as context:
            tool.make_job_runner(runtimeContext)
        self.assertIn('no default_container', str(context.exception))

    def test_injects_default_container(self):
        self.fail()
