import pymssql

class Connect:
    def __init__(self,hostname='hostname',username='yourname',password='yourpassword',database='yourdatabase',charset='utf8mb4'):

        self.dict = {}
        self.connection = pymssql.connect(hostname,
                                          username,  # 这里输入sqlserver用户名
                                          password,  # 这里输入sqlserver密码
                                          database)# 这里输入sqlserver库名


    def EveryDay_Class(self,date):
        #通过date找到教学班 ，通过教学班找到所有属于这个教学班的学生，返回学生课程名，课程开始时间，结束时间，openID字典
        """
        {
        openID:[[TeacherClassID，courseName,StartTime,EndTime],[]]

        :param date:
        :return:
        """
        try:
            with self.connection.cursor(as_dict=True) as cursor:
                    # Create a new record
                    sql = "SELECT [TeachClassID], [CourseID] ,[CourseName],[ClassStart] ,[ClassEnd] ,[ClassRoom] " \
                          "FROM [tb_TimeTable] " \
                          "WHERE Date = %s"
                    print(sql)
                    cursor.execute(sql, date)
                    teacherClassids = cursor.fetchall()

                    print(teacherClassids)

                    for i in range(0, len(teacherClassids)):
                        thisClass = teacherClassids[i]
                        thisClass_TeacherClassID = thisClass['TeachClassID'] #找到教学班ID

                        s = "SELECT [StuID],[StuName],[OpenID] FROM [tb_StuInfo] WHERE TeachClassIDs LIKE '%%%s%%'"
                        print(s%thisClass_TeacherClassID)
                        cursor.execute(s%thisClass_TeacherClassID)
                        Student = cursor.fetchall() #学生信息
                        print("总计"+str(len(Student)))

                        for i in range(0,len(Student)):
                            thisStudent = Student[i]

                            print(thisStudent)

                            thisStudentOpenID = thisStudent['OpenID']

                            classInformation = [thisStudent['StuID'],thisStudent['StuName'],thisClass['CourseName'],thisClass['ClassStart'],thisClass['ClassEnd'],thisClass['ClassRoom']]
                            print(classInformation)

                            self.dict.setdefault(thisStudentOpenID,[]).append(classInformation)


                    self.connection.commit()
        except Exception as e:
            print(e)
        finally:
            self.connection.close()
            return self.dict

if __name__ =='__main__':
    s=Connect()
    h=s.EveryDay_Class("20180510")
    print(h)

