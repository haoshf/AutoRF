# coding=utf-8
import os
import json
from repository import models
import datetime

class Building(object):

    def __init__(self):
        pass

    def build_testcase(self,caseids,runCase):
        suite_list = []
        suitefile_list = []
        buil_resource = []
        filepath = '%s/robot/%s/'%(os.getcwd().replace('\\','/'),runCase)
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        with open('%sargfile.txt'%filepath,'w',encoding='utf8') as arg:
            arg.write('-C\noff\n-W\n222')
            for caseid in caseids:
                case = models.Testcase.objects.filter(id=caseid).first()
                suite = models.Suite.objects.filter(id=case.suite_id).first()
                resource = suite.Resource
                resource_list = eval(resource)
                resource = models.Resource.objects.filter(id__in=resource_list)
                for res in list(resource):
                    resource_list2 = res.Resource
                    if resource_list2:
                        resource2 = models.Resource.objects.filter(id__in=eval(resource_list2))
                        for r in resource2:
                            print('r--->', r.id)
                            self.build_resource(r,filepath,buil_resource)

                    self.build_resource(res,filepath,buil_resource)

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
                        print('......')
                    self.build_suite_basic(filepath_name, suite, resource,filepath,buil_resource,runCase)

                with open(filepath_name, 'a', encoding='utf-8') as f:
                    arg.write('\n--test\n%s.%s.%s' %(runCase,sort + suite.suite_name,case.testcase_name))
                    f.write("\n%s"%case.testcase_name)
                    if case.Documentation:
                        f.write('\n    [Documentation]    ' + case.Documentation.replace('\n',''))
                    if case.Tags:
                        f.write('\n    [Tags]    ' + case.Tags.replace('|','    '))
                    if case.Setup:
                        f.write('\n    [Setup]    ' + case.Setup.replace('|','    '))
                    if case.Template:
                        f.write('\n    [Template]    ' + case.Template.replace('|','    '))
                    if case.Timeout:
                        f.write('\n    [Timeout]    ' + case.Timeout.replace('|','    '))
                    f.write('\n')
                    table_size = {'tr': [1], 'td': [1]}
                    table_tr_list = self.deal_table(json.loads(case.Table_value),table_size)
                    for table_tr in table_tr_list:
                        for table_td in table_tr:
                            f.write('    %s' % table_td)
                        f.write('\n')
                    if case.Teardown:
                        f.write('\n    [Teardown]    ' +  case.Teardown.replace('|','    '))

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

    def build_resource(self,resource_obj,filepath,buil_resource):
        work_path = os.getcwd().replace('\\', '/')
        file_name = filepath.split('/')[-2]
        print('sssssssssssssaaa',resource_obj.resource_name)
        filepath_name = '%s%s.robot'%(filepath,resource_obj.resource_name)
        if resource_obj.resource_name in buil_resource:
            print('当前已构建过！')
            return '资源构建完成！'
        elif os.path.exists(filepath_name) and file_name.isdigit():
            os.remove(filepath_name)
        elif os.path.exists(filepath_name):
            print('其它地方已构建过')
            return '资源构建完成！'

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
                if Library.library_name[-2:] == 'py':
                    f.write("\nLibrary       " +work_path+ Library.filepath)
                else:
                    f.write("\nLibrary       " +Library.filepath)
            for Res in Resource:
                f.write("\nResource       %s.robot"%Res)
            if resource_obj.Scalar_Variables or resource_obj.List_Variables or resource_obj.Dict_Variables:
                f.write('\n*** Variables ***\n')
                for Variables in resource_obj.Scalar_Variables.split('|'):
                    f.write(Variables.replace('=','    ') + '\n')
                for Variables in resource_obj.List_Variables.split('|'):
                    f.write(Variables.replace('=','    ') + '\n')
                for Variables in resource_obj.Dict_Variables.split('|'):
                    f.write(Variables.replace('=','    ') + '\n')
            f.write("\n\n*** Keywords ***")
            for word in keywords:
                print('word.keyword_name=============',word.keyword_name)
                f.write("\n%s"%word.keyword_name)
                if word.Arguments:
                    f.write('\n    [Arguments]    ' + word.Arguments.replace('|','    '))
                if word.Documentation:
                    f.write('\n    [Documentation]    ' + word.Documentation.replace('\n',''))
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
                    f.write('    [Return]    ' + word.Return_Value.replace('|','    ')+'\n')

        buil_resource.append(resource_obj.resource_name)
        return '资源构建完成！'

    def build_suite_basic(self,filepath_name,suite_obj,resource,filepath,buil_resource,runCase):

        work_path = os.getcwd().replace('\\', '/')
        project = models.Project.objects.filter(id=suite_obj.project_id).first()
        Library_list = []
        if project.Library:
            Library_list = models.Library.objects.filter(id__in=eval(project.Library))
        resource_list = []
        if project.Resource:
            resource_list = models.Resource.objects.filter(id__in=eval(project.Resource))
            for res in list(resource_list):
                resource_list2 = res.Resource
                if resource_list2:
                    resource2 = models.Resource.objects.filter(id__in=eval(resource_list2))
                    for r in resource2:
                        print('r--->', r.id)
                        self.build_resource(r, filepath,buil_resource)
                self.build_resource(res, filepath,buil_resource)
        with open('%s__init__.robot'%filepath, 'w', encoding='utf-8') as f:
            f.write("*** Settings ***")
            if project.Documentation:
                f.write('\nDocumentation        ' + project.Documentation.replace('\n',''))
            if project.Suite_Setup:
                user = models.UserInfo.objects.filter(id=runCase).first()
                for account in json.loads(user.projectAccount):
                    print(account)
                    print(project.id)
                    if str(account['project_id']) == str(project.id):
                        Suite_Setup = '    '.join(project.Suite_Setup.split('|')[:1]+account['projectAccount'].split('|'))
                        f.write('\nSuite Setup        ' + Suite_Setup)
                        break
                else:
                    f.write('\nSuite Setup        ' + project.Suite_Setup.replace('|','    '))
            if project.Suite_Teardown:
                f.write('\nSuite Teardown        ' + project.Suite_Teardown.replace('|','    '))
            if project.Test_Setup:
                f.write('\nTest Setup        ' + project.Test_Setup.replace('|','    '))
            if project.Test_Teardown:
                f.write('\nTest Teardown        ' + project.Test_Teardown.replace('|','    '))
            if project.Force_Tags:
                f.write('\nForce Tags        ' + project.Force_Tags.replace('|','    '))
            for Library in Library_list:
                if Library.library_name[-2:] == 'py':
                    f.write("\nLibrary       " +work_path+ Library.filepath)
                else:
                    f.write("\nLibrary       " +Library.filepath)
            for res in resource_list:
                f.write("\nResource       %s.robot"%res.resource_name)

            if project.Scalar_Variables or project.List_Variables or project.Dict_Variables:
                f.write('\n*** Variables ***\n')
                for Variables in project.Scalar_Variables.split('|'):
                    f.write(Variables.replace('=','    ') + '\n')
                for Variables in project.List_Variables.split('|'):
                    f.write(Variables.replace('=','    ') + '\n')
                for Variables in project.Dict_Variables.split('|'):
                    f.write(Variables.replace('=','    ') + '\n')
        Library_list = []
        if suite_obj.Library:
            Library_list = models.Library.objects.filter(id__in=eval(suite_obj.Library))
        with open(filepath_name, 'w', encoding='utf-8') as f:
            f.write("*** Settings ***")
            if suite_obj.Documentation:
                f.write('\nDocumentation        ' + suite_obj.Documentation.replace('\n',''))
            if suite_obj.Suite_Setup:
                f.write('\nSuite Setup        ' + suite_obj.Suite_Setup.replace('|','    '))
            if suite_obj.Suite_Teardown:
                f.write('\nSuite Teardown        ' + suite_obj.Suite_Teardown.replace('|','    '))
            if suite_obj.Test_Setup:
                f.write('\nTest Setup        ' + suite_obj.Test_Setup.replace('|','    '))
            if suite_obj.Test_Teardown:
                f.write('\nTest Teardown        ' + suite_obj.Test_Teardown.replace('|','    '))
            if suite_obj.Force_Tags:
                f.write('\nForce Tags        ' + suite_obj.Force_Tags.replace('|','    '))
            if suite_obj.Default_Tags:
                f.write('\nDefault Tags        ' + suite_obj.Default_Tags.replace('|','    '))
            if suite_obj.Test_Template:
                f.write('\nTest Template        ' + suite_obj.Test_Template.replace('|','    '))
            if suite_obj.Test_Timeout:
                f.write('\nTest Timeout        ' + suite_obj.Test_Timeout.replace('|','    '))
            for Library in Library_list:
                if Library.library_name[-2:] == 'py':
                    f.write("\nLibrary       " +work_path+ Library.filepath)
                else:
                    f.write("\nLibrary       " +Library.filepath)
            for res in resource:
                f.write("\nResource       %s.robot"%res.resource_name)

            if suite_obj.Scalar_Variables or suite_obj.List_Variables or suite_obj.Dict_Variables:
                f.write('\n*** Variables ***\n')
                for Variables in suite_obj.Scalar_Variables.split('|'):
                    f.write(Variables.replace('=','    ') + '\n')
                for Variables in suite_obj.List_Variables.split('|'):
                    f.write(Variables.replace('=','    ') + '\n')
                for Variables in suite_obj.Dict_Variables.split('|'):
                    f.write(Variables.replace('=','    ') + '\n')
            f.write("\n\n*** Test Cases ***")

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
            'status': '',
            'user':user_id,
            'start_time':datetime.datetime.now(),
            'take_time':'',
            'report_path':'',
            'log_path': '/robot/%s/'% runCase
        }
        task = models.Task.objects.create(**dic)
        caseid_list = []
        for suite in suites:
            caseids = models.Testcase.objects.filter(suite=suite).order_by('sort')
            for caseid in caseids:
                caseid_list.append(caseid.id)
        filepath = self.build_testcase(caseid_list,runCase)
        return filepath,task.id

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
            caseids = models.Testcase.objects.filter(suite=suite).order_by('sort')

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
                'status': '',
                'user': user_id,
                'start_time': datetime.datetime.now(),
                'take_time': '',
                'report_path': '',
                'log_path': '/robot/%s/' % runCase
            }
            print('xxxxxxxxxxxxxx',dic)

            task = models.Task.objects.create(**dic)
            filepath = self.build_testcase(caseid_list, runCase)
            return filepath,task.id