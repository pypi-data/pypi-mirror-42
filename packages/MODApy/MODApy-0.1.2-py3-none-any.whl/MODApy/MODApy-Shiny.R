library(shiny)
library(ConfigParser)
library(reticulate)

# python config -------------------------------------------------------------------
cfgpath = '/DiscoDatos/Development/modapy/MODApy/config.ini'
logfile = "/DiscoDatos/Development/modapy/MODApy/logs/currentrun.log"
cfg = read.ini(cfgpath)
use_virtualenv("/DiscoDatos/Development/modapy/venv/")
use_python("/DiscoDatos/Development/modapy/venv/python3")
py_config()


# combo box options -------------------------------------------------------------------
patientsvcf <- gsub('\\..*','',basename(list.files(cfg$PATHS$patientpath,pattern="\\.final.vcf",recursive = TRUE)))

# utils ---------------------------------------------------------------------------
getcommand <- function(input){
  cmd = ''
  switch (input$tabset,
          Pipeline={
            if(file.exists(paste(cfg$PATHS$patientpath, input$PatientPipe, "/",input$PatientPipe,"_1", ".fastq", sep=""))){
              cmd =  paste("pipeline -Pipeline", 
                           input$Pipeline, "-FQ", 
                           paste(input$PatientPipe, "/",input$PatientPipe,"_1", ".fastq", sep=""), "-FQ",
                           paste(input$PatientPipe, "/",input$PatientPipe,"_2", ".fastq", sep=""))
            }
            else if(file.exists(paste(cfg$PATHS$patientpath, input$PatientPipe, "/",input$PatientPipe,"_1", ".fastq.gz", sep=""))){
              cmd = paste("pipeline -Pipeline", 
                          input$Pipeline, "-FQ", 
                          paste(input$PatientPipe, "/",input$PatientPipe,"_1", ".fastq.gz", sep=""), "-FQ",
                          paste(input$PatientPipe, "/",input$PatientPipe,"_2", ".fastq.gz", sep=""))
            }
            else {
              cat("No fastq or gzipped fastq files found for that Patient",file=logfile,sep='\n')
            }
          },
          Panel={
              cmd = paste("single -Panel", input$Panel, "-Patient", paste(input$PatientPanel, "/",input$PatientPanel,".final.vcf", sep=""))
            },
          Duos={
            cmd = paste("duos -Patient1", paste(input$Patient1D, "/",input$Patient1D,".final.vcf", sep=""), "-Patient2", paste(input$Patient2D, "/",input$Patient2D,".final.vcf", sep=""), '--Filter')
            if(input$vennplaceD == input$Patient1D){venn = "A"}
            else if(input$vennplaceD == input$Patient2D){venn = "B"}
            else if(input$vennplaceD == paste(input$Patient1D,input$Patient2D,sep=":")){venn = "A:B"}
            if(exists("venn")){
              cmd = paste(cmd,"--VennPlace", venn)
            }
            if(input$PanelD != 'NONE'){
              cmd = paste(cmd, '--Panel', input$PanelD)
            }
          },
          Trios={
            cmd = cmd = paste("trios -Patient1", paste(input$Patient1T, "/",input$Patient1T,".final.vcf", sep=""), "-Patient2", paste(input$Patient2T, "/",input$Patient2T,".final.vcf", sep=""), "-Patient3", paste(input$Patient3T, "/",input$Patient3T,".final.vcf", sep=""), '--Filter')
            if(input$vennplaceT == input$Patient1T){venn = "A"}
            else if(input$vennplaceT == input$Patient2T){venn = "B"}
            else if(input$vennplaceT == input$Patient3T){venn = "C"}
            else if(input$vennplaceT == paste(input$Patient1T,input$Patient2T,sep=":")){venn = "A:B"}
            else if(input$vennplaceT == paste(input$Patient1T,input$Patient3T,sep=":")){venn = "A:C"}
            else if(input$vennplaceT == paste(input$Patient2T,input$Patient3T,sep=":")){venn = "B:C"}
            else if(input$vennplaceT == paste(input$Patient1T,input$Patient2T,input$Patient3T,sep=":")){venn = "A:B:C"}
            if(exists("venn")){
              cmd = paste(cmd,"--VennPlace", venn)
            }
            if(input$PanelT != 'NONE'){  
              cmd = paste(cmd, '--Panel', input$PanelT)
            }
          }
  )
  cmd <- gsub("[(]","\\\\(",cmd)
  cmd <- gsub("[)]","\\\\)",cmd)
  system2("MODApy", cmd ,wait=FALSE)
}

# ui -------------------------------------------------------------------
panels = 
ui <- fluidPage(
  tags$head(
    tags$style(HTML("
      @import url('//fonts.googleapis.com/css?family=Courgette|Cabin:400,700');
    "))
  ),
  titlePanel("", windowTitle = "MODApy"),
  headerPanel(
    fluidRow(
      h1("MODApy", 
         style = "font-family: 'Courgette', cursive;
        font-weight: 500; line-height: 1.1; 
        color: #4d3a7d;"),
      h3("Multi-Omics Data Analysis in Python"),
      h3("R User Interface"))
  ),
  sidebarLayout(
    sidebarPanel(
      width = 6,
      tabsetPanel(id="tabset", selected = "Panel",
        # tabPanel("Pipeline",
        #   selectInput(inputId = "Pipeline", label = "Pipelines", choices = list.files(path=cfg$PATHS$pipelinespath)),
        #   selectInput(inputId = "PatientPipe", label = "Patient", choices = list.dirs(
        #     path = cfg$PATHS$patientpath ,full.names = FALSE,recursive = FALSE))
        # ),
        tabPanel("Panel",
          selectInput(inputId = "PatientPanel", label = "Patient", choices = patientsvcf),
          selectInput(inputId = "Panel", label = "Panel", choices = gsub('.xlsx','',list.files(path=cfg$PATHS$panelspath)))
        ),
        tabPanel("Duos",
          selectInput(inputId = "Patient1D", label = "Patient 1", choices = patientsvcf),
          selectInput(inputId = "Patient2D", label = "Patient 2", choices = patientsvcf),
          selectInput(inputId = "PanelD", label = "Panel (optional)", choices = gsub('.xlsx',"",c('NONE',list.files(path=cfg$PATHS$panelspath))), selected='NONE'),
          uiOutput("vennDuos")
        ),
        tabPanel("Trios",
          selectInput(inputId = "Patient1T", label = "Patient 1", choices = patientsvcf),
          selectInput(inputId = "Patient2T", label = "Patient 2", choices = patientsvcf),
          selectInput(inputId = "Patient3T", label = "Patient 3", choices = patientsvcf),
          selectInput(inputId = "PanelT", label = "Panel (optional)", choices = gsub('.xlsx',"",c('NONE',list.files(path=cfg$PATHS$panelspath))), selected='NONE'),
          uiOutput("vennTrios")
        )
      ),
      actionButton("buttonrun","Run"),
      actionButton("buttonlastcmd","Get Last Command Status")
    ),
    mainPanel(#style="background-color:blue",
      width = 6,
      h1('Command Output',style = "font-family: 'Courgette', cursive;
        font-weight: 500; line-height: 1.1; 
        color: #4d3a7d;"),
      htmlOutput("consoleout")
    )
  )
)
# server -------------------------------------------------------------------
server <- function(input,output, session){
  rv <- reactiveValues(textstream = c(""), timer = reactiveTimer(1000),started=FALSE)
  
  observeEvent(input$buttonrun, {
    rv$started<-TRUE
    getcommand(input)
  })
  observeEvent(input$buttonlastcmd, {
    rv$started<-TRUE
  })
  observe({
    rv$timer()
    if(isolate(rv$started))rv$textstream <- paste(readLines(logfile),collapse="<br/>")
  })
  output$consoleout <- renderUI({
    HTML(rv$textstream)
  })
   output$vennDuos <- renderUI({
    selectInput("vennplaceD","Venn Place:", choices = list(input$Patient1D, input$Patient2D, paste(input$Patient1D, input$Patient2D,sep=":"), "All"), selected='All')
  })
  output$vennTrios <- renderUI({
    selectInput("vennplaceT","Venn Place:", choices = list(input$Patient1T, input$Patient2T, input$Patient3T, paste(input$Patient1T, input$Patient2T,sep=":"), paste(input$Patient1T, input$Patient3T,sep=":"), paste(input$Patient2T, input$Patient3T,sep=":"), paste(input$Patient1T, input$Patient2T, input$Patient3T,sep=":"), "All"), selected='All')
  })
  session$onSessionEnded(function(){stopApp()})
}
  
shinyApp(ui = ui, server = server)