TEMPLATE_LOC = "output/winrateTemplate.html"

def writeTimeOutput(outFile,timeHist):
    template = open(TEMPLATE_LOC).read()
    template = template.replace("%%xlabels%%",",".join(str(k) for k in sorted(timeHist.keys())))
    template = template.replace("%%winrates%%",",".join(str(timeHist[k]) for k in sorted(timeHist.keys())))
    template = template.replace("%%title%%","Win rate over time")
    with open(outFile,'w') as out:
        out.write(template)
