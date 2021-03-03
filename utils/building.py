# coding=utf-8
import os
import json
from repository import models
import datetime

class Building(object):

    def __init__(self):
        pass

    def build_testcase(self,caseids,runCase):
        testcase_list = models.Testcase.objects.filter(id__in=caseids)
        suite_list = []
        suitefile_list = []
        filepath = '%s/robot/%s/'%(os.getcwd().replace('\\','/'),runCase)
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        with open('%sargfile.txt'%filepath,'w',encoding='utf8') as arg:
            arg.write('-C\noff\n-W\n222')
            for case in testcase_list:
                suite = models.Suite.objects.filter(id=case.suite_id).first()
                resource = suite.Resource
                resource_list = eval(resource)
                resource = models.Resource.objects.filter(id__in=resource_list)
                print('resource--->',resource)
                for res in list(resource):
                    resource_list2 = eval(res.Resource)
                    resource2 = models.Resource.objects.filter(id__in=resource_list2)
                    print('resource2--->', resource2)

                    for r in resource2:
                        print('r--->', r)
                        self.build_resource(r,filepath)

                    self.build_resource(res,filepath)

                sort = str(suite.sort)
                if int(suite.sort) < 10:
                    sort = '0' + sort
                filepath_name = '%s%s.robot'%(filepath,sort + suite.suite_name)
                arg.write('\n--suite\n%s.%s'%(runCase,sort+ suite.suite_name))
                print('suite_list',suite_list)
                if suite not in suite_list:
                    print('?????????????????????????',filepath_name)
                    suite_list.append(suite)

                    if os.path.exists(filepath_name):
                        os.remove(filepath_name)
                    self.build_suite_basic(filepath_name, suite, resource,filepath)

                with open(filepath_name, 'a', encoding='utf-8') as f:
                    arg.write('\n--test\n%s.%s.%s' %(runCase,sort + suite.suite_name,case.testcase_name))
                    f.write("\n%s"%case.testcase_name)
                    if case.Documentation:
                        f.write('\n    [Documentation]    ' + case.Documentation)
                    if case.Tags:
                        f.write('\n    [Tags]    ' + '    '.join(eval(case.Tags)))
                    if case.Setup:
                        f.write('\n    [Setup]    ' + '    '.join(eval(case.Setup)))
                    if case.Template:
                        f.write('\n    [Template]    ' + '    '.join(eval(case.Template)))
                    if case.Timeout:
                        f.write('\n    [Timeout]    ' + case.Timeout)
                    f.write('\n')
                    table_size = {'tr': [1], 'td': [1]}
                    table_tr_list = self.deal_table(json.loads(case.Table_value),table_size)
                    for table_tr in table_tr_list:
                        for table_td in table_tr:
                            f.write('    %s' % table_td)
                        f.write('\n')
                    if case.Teardown:
                        f.write('\n    [Teardown]    ' + '    '.join(eval(case.Teardown)))

                suitefile_list.append(filepath_name)
        suite_list = []
        return filepath

    def deal_table(self,Table_value,table_size):


        table_tr_list = []
        table_td_list = []
        table_tr=0
        table_td=0
        for size in Table_value.keys():
            table_tr_list.append(int(size.split('-')[0]))
            table_td_list.append(int(size.split('-')[1]))

        if table_tr_list != []:
            table_tr = sorted(table_tr_list)[-1]
            table_td = sorted(table_td_list)[-1]
        if table_tr > len(table_size['tr']):
            for i in range(len(table_size['tr']) + 1, table_tr + 1):
                table_size['tr'].append(i)

        if table_td > len(table_size['td']):
            for i in range(len(table_size['td']) + 1, table_td + 1):
                table_size['td'].append(i)
        table_tr_list = []
        for i in table_size['tr']:
            table_td_list = []
            for j in table_size['td']:
                key = '{0}-{1}'.format(str(i), str(j))
                if key not in Table_value.keys():
                    table_td_list.append('')
                else:
                    table_td_list.append(Table_value[key])
            table_tr_list.append(table_td_list)
        return table_tr_list

    def build_resource(self,resource_obj,filepath):
        filepath_name = '%s%s.robot'%(filepath,resource_obj.resource_name)
        if os.path.exists(filepath_name):
            os.remove(filepath_name)
        keywords = models.Keyword.objects.filter(resource=resource_obj.id).all()
        Resource = models.Resource.objects.filter(id__in=eval(resource_obj.Resource))
        Library_list = []
        if resource_obj.Library:
            Library_list = models.Library.objects.filter(id__in=eval(resource_obj.Library))
        with open(filepath_name, 'w',encoding='utf-8') as f:
            f.write("*** Settings ***")
            if resource_obj.Documentation:
                f.write('\nDocumentation    ' + resource_obj.Documentation)
            for Library in Library_list:
                f.write("\nLibrary       " + Library.filepath)
            for Res in Resource:
                f.write("\nResource       ./%s.robot"%Res)
            f.write("\n\n*** Keywords ***")
            for word in keywords:
                print('word.keyword_name=============',word.keyword_name)
                f.write("\n%s"%word.keyword_name)
                if word.Arguments:
                    f.write('\n    [Arguments]    ' + '    '.join(eval(word.Arguments)))
                if word.Documentation:
                    f.write('\n    [Documentation]    ' + word.Documentation)
                if word.Tags:
                    f.write('\n    [Tags]    ' + '    '.join(eval(word.Tags)))
                if word.Timeout:
                    f.write('\n    [Timeout]    ' + word.Timeout)
                f.write('\n')
                table_size = {'tr': [1], 'td': [1]}
                table_tr_list = self.deal_table(json.loads(word.Table_value),table_size)
                for table_tr in table_tr_list:
                    for table_td in table_tr:
                        f.write('    %s' % table_td)
                    f.write('\n')
                if word.Teardown:
                    f.write('\n    [Teardown]    ' + '    '.join(eval(word.Teardown)))
                if word.Return_Value:
                    f.write('    [Return]    ' + '    '.join(eval(word.Return_Value)))

        return '资源构建完成！'

    def build_suite_basic(self,filepath_name,suite_obj,resource,filepath):

        project = models.Project.objects.filter(id=suite_obj.project_id).first()
        Library_list = []
        if project.Library:
            Library_list = models.Library.objects.filter(id__in=eval(project.Library))
        with open('%s__init__.robot'%filepath, 'w', encoding='utf-8') as f:
            f.write("*** Settings ***")
            if project.Documentation:
                f.write('\nDocumentation        ' + project.Documentation)
            if project.Suite_Setup:
                f.write('\nSuite Setup        ' + '    '.join(eval(project.Suite_Setup)))
            if project.Suite_Teardown:
                f.write('\nSuite Teardown        ' + '    '.join(eval(project.Suite_Teardown)))
            if project.Test_Setup:
                f.write('\nTest Setup        ' + '    '.join(eval(project.Test_Setup)))
            if project.Test_Teardown:
                f.write('\nTest Teardown        ' + '    '.join(eval(project.Test_Teardown)))
            if project.Force_Tags:
                f.write('\nForce Tags        ' + '    '.join(eval(project.Force_Tags)))
            for Library in Library_list:
                f.write("\nLibrary       " + Library.filepath)
            for res in resource:
                f.write("\nResource       ./%s.robot"%res.resource_name)

        Library_list = []
        if suite_obj.Library:
            Library_list = models.Library.objects.filter(id__in=eval(suite_obj.Library))
        with open(filepath_name, 'w', encoding='utf-8') as f:
            f.write("*** Settings ***")
            if suite_obj.Documentation:
                f.write('\nDocumentation        ' + suite_obj.Documentation)
            if suite_obj.Suite_Setup:
                f.write('\nSuite Setup        ' + '    '.join(eval(suite_obj.Suite_Setup)))
            if suite_obj.Suite_Teardown:
                f.write('\nSuite Teardown        ' + '    '.join(eval(suite_obj.Suite_Teardown)))
            if suite_obj.Test_Setup:
                f.write('\nTest Setup        ' + '    '.join(eval(suite_obj.Test_Setup)))
            if suite_obj.Test_Teardown:
                f.write('\nTest Teardown        ' + '    '.join(eval(suite_obj.Test_Teardown)))
            if suite_obj.Force_Tags:
                f.write('\nForce Tags        ' + '    '.join(eval(suite_obj.Force_Tags)))
            if suite_obj.Default_Tags:
                f.write('\nDefault Tags        ' + '    '.join(eval(suite_obj.Default_Tags)))
            if suite_obj.Test_Template:
                f.write('\nTest Template        ' + '    '.join(eval(suite_obj.Test_Template)))
            if suite_obj.Test_Timeout:
                f.write('\nTest Timeout        ' + suite_obj.Test_Timeout)
            for Library in Library_list:
                f.write("\nLibrary       " + Library.filepath)
            for res in resource:
                f.write("\nResource       ./%s.robot"%res.resource_name)

            f.write("\n\n*** Test Cases ***")

            #参数变量待处理
            # if suite_obj.Scalar_Variables:
            #     for k,v in suite_obj.Scalar_Variables:
            #         f.write("\n\n*** Variables ***" + res.resource_name)
        return '套件基础构建完成！'

    def build_project(self,project_id,user_id):
        start = datetime.datetime.now().strftime('%y-%m-%d_%H%M%S')
        project = models.Project.objects.filter(id=project_id).first()
        runCase = project.project_name +'_'+ start
        suites = models.Suite.objects.filter(project=project_id).order_by('suite_name').order_by('sort')
        if not suites:
            return 'Suite',False
        dic = {
            'task_name':project,
            'documentation':[suite.suite_name for suite in suites],
            'status': '运行中',
            'user':user_id,
            'start_time':datetime.datetime.now(),
            'take_time':'',
            'report_path':'',
            'log_path': '/robot/%s/'% runCase
        }
        task = models.Task.objects.create(**dic)
        caseid_list = []
        for suite in suites:
            caseids = models.Testcase.objects.filter(suite=suite)
            if not caseids:
                return 'Case', False
            for caseid in caseids:
                caseid_list.append(caseid.id)
        filepath = self.build_testcase(caseid_list,runCase)
        return filepath,task

    def build_suite(self,suite_ids,user_id):
        start = datetime.datetime.now().strftime('%y-%m-%d_%H%M%S')
        print('////////////',suite_ids)
        suites = models.Suite.objects.filter(id__in=suite_ids).all()
        print('suite_ids',suite_ids)
        projects = []
        caseid_list = []
        for suite in suites:
            project = models.Project.objects.filter(id=suite.project_id).first()
            projects.append(project.id)
            caseids = models.Testcase.objects.filter(suite=suite)
            if not caseids:
                return 'Case', False
            for caseid in caseids:
                caseid_list.append(caseid.id)
        projects = list(set(projects))
        if len(projects) >1:
            return False
        else:
            runCase = project.project_name + '_' + start
            dic = {
                'task_name': project,
                'documentation': [suite.suite_name for suite in suites],
                'status': '运行中',
                'user': user_id,
                'start_time': datetime.datetime.now(),
                'take_time': '',
                'report_path': '',
                'log_path': '/robot/%s/' % runCase
            }
            task = models.Task.objects.create(**dic)

            filepath = self.build_testcase(caseid_list, runCase)
            return filepath,task