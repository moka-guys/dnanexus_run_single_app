'''
Created on 9 Dec 2016

@author: aled
'''
import subprocess

class Redo_coverage(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        # result of the command dx find data --name "*1.bam" --path NGS_runs:/ > all_bams.txt and dx find data --name "*1.bai" --path NGS_runs:/ >> all_bams.txt
        self.list_of_bams="/home/aled/Documents/redo_coverage/all_bams.txt"
        #output file
        self.shellscript="/home/aled/Documents/redo_coverage/re_do.sh"
        #empty lists
        self.templist=[]
        self.list=[]
        
        # for the sh script
        #project for the output files and the location of the workflow  
        self.app_project="003_161208_Coverage:"
        #set the environment
        self.initiate = "#!/bin/bash\nsource /etc/profile.d/dnanexus.environment.sh.off\n"
        # define where the project is
        self.base_command = "dx run "+self.app_project+"GATK3_DiagnoseTargets_161209 -y"
        # each stage input
        self.arg1 = " -istage-F14bY8j0Z7741Bp91pQJ1yFJ.sorted_bam=NGS_runs:"
        self.arg2 = " -istage-F14bY8j0Z7741Bp91pQJ1yFJ.bam_index=NGS_runs:"
        # where the output file are going
        self.arg5 = " --dest="+self.app_project
        #token (This should be able to see all the projects used, including files used within a workflow)
        self.arg6 = " --brief --auth-token <put auth token here>\n"
        
    
    def read_bam_list(self):
        #open list of bams
        with open(self.list_of_bams,'r') as bams:
            for line in bams:
                #capture the file tag
                file_tag=line.split('(')[1].replace(')',"").rstrip()
                #capture the full path to the file
                project=line.split('(')[0].split(' /')[1]
                #append to the temp list
                self.templist.append((project,file_tag))
        #count for checking
        count=0
        for i in self.templist:
            # each bam file should have a .bai file so for each bam find the file tag for the bai
            filename=i[0]
            if filename.rstrip().endswith(".bam"):
                #define name of the index
                bai=filename.replace(".bam",".bai")
                # look up index in list
                for j in self.templist:
                    if bai in j[0]:
                        #append the project folder, bam and bai hashes to list
                        self.list.append((i[0].split('/')[0],i[1],j[1]))
                        
        #print self.list
        
    def write_shellscript(self):
        # open the shell script
        shell=open(self.shellscript,'w')
        # write the command to source env
        shell.write(self.initiate)
        #loop through the list and build the dx run command
        for file in self.list:
            shell.write(self.base_command+self.arg1+file[1]+self.arg2+file[2]+self.arg5+file[0]+self.arg6)
        shell.close()
            
if __name__ == "__main__":
    a=Redo_coverage()
    a.read_bam_list()
    a.write_shellscript()