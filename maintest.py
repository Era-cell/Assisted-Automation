from Testing.access import Job

def getjob(company='amd'):
    joblist=[]
    while not joblist:
        try:
            with Job() as bot:

                bot.land_first_page()
                bot.chooseType("engineering")
                bot.applyfilter()
                joblist = bot.getJobList()
        except Exception as e:
            if 'in PATH' in str(e):
                print("You are trying to execute program from command line")
            else:
                raise
    return joblist
print(getjob())