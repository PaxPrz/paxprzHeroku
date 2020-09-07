var init_script = `
[ <span class="success">OK</span> ] Started Authorization Manager. <!--asdfljskdfjlsasdfasdfasdf-->
[ <span class="success">OK</span> ] Started Accounts Service. <!--asdfljskdfjlsasdfasdfasdf-->
[ <span class="success">OK</span> ] Started Network Service. <!--asdfljskdfjlsasdfasdfasdf-->
[ <span class="success">OK</span> ] Loaded Library Files. <!--asdfljskdfjlsasdfasdfasdf-->
[ <span class="success">OK</span> ] Starting Terminal. <!--asdfljskdfjlsasdfasdfasdf-->
`;

// var init_script = 'hello';

var LoginScript = `
PaxPrz System terminal <!--nextline-->
Enter Username : `;

// var writer = setInterval('write(init_script);', 10);
// var index = 0;

function write(word) {
    if (index >= word.length - 1) {
        clearInterval(writer);
    }
    $('#console').append(word[index]);
    index++;
}

var Typer = {
    text: '',
    accessCountimer: null,
    index: 0,
    speed: 2,
    file: '',
    accessCount: 0,
    deniedCount: 0,
    init: function (text) {
        //   accessCountimer = setInterval(function () {
        //     Typer.updLstChr();
        //   }, 500);
        Typer.index = 0;
        Typer.text = text;
        //   $.get(Typer.file, function (data) {

        //     Typer.text = Typer.text.slice(0, Typer.text.length - 1);
        //   });
    },

    content: function () {
        return $('#console').html();
    },

    write: function (str) {
        $('#console').append(str);
        return false;
    },

    addText: function (key) {
        if (key.keyCode == 18) {
            Typer.accessCount++;

            if (Typer.accessCount >= 3) {
                Typer.makeAccess();
            }
        } else if (key.keyCode == 20) {
            Typer.deniedCount++;

            if (Typer.deniedCount >= 3) {
                Typer.makeDenied();
            }
        } else if (key.keyCode == 27) {
            Typer.hidepop();
        } else if (Typer.text) {
            var cont = Typer.content();
            if (cont.substring(cont.length - 1, cont.length) == '|')
                $('#console').html(
                    $('#console')
                        .html()
                        .substring(0, cont.length - 1),
                );
            if (key.keyCode != 8) {
                Typer.index += Typer.speed;
            } else {
                if (Typer.index > 0) Typer.index -= Typer.speed;
            }
            var text = Typer.text.substring(0, Typer.index);
            var rtn = new RegExp('\n', 'g');

            $('#console').html(text.replace(rtn, '<br/>'));
            window.scrollBy(0, 50);
        }

        if (key.preventDefault && key.keyCode != 122) {
            key.preventDefault();
        }

        if (key.keyCode != 122) {
            // otherway prevent keys default behavior
            key.returnValue = false;
        }
    },

    updLstChr: function () {
        var cont = this.content();

        if (cont.substring(cont.length - 1, cont.length) == '|')
            $('#console').html(
                $('#console')
                    .html()
                    .substring(0, cont.length - 1),
            );
        else this.write('|'); // else write it
    },
};

function replaceUrls(text) {
    var http = text.indexOf('http://');
    var space = text.indexOf('.me ', http);

    if (space != -1) {
        var url = text.slice(http, space - 1);
        return text.replace(url, '<a href="' + url + '">' + url + '</a>');
    } else {
        return text;
    }
}

var DEBUG = true;

function BootUp() {
    Typer.init(init_script);
    return new Promise((resolve, reject) => {
        var timer = setInterval(() => {
            Typer.addText({ keyCode: 123748 });

            if (Typer.index > Typer.text.length) {
                clearInterval(timer);
                if (DEBUG) console.log('OK-2');
                resolve('ok');
            }
        }, 30);
    });
}

function UserLogin() {
    Typer.init(LoginScript);
    $('#console').empty();
    return new Promise((resolve, reject) => {
        var timer = setInterval(() => {
            Typer.addText({ keyCode: 123748 });

            if (Typer.index > Typer.text.length) {
                clearInterval(timer);
                if (DEBUG) console.log('OK-2');
                resolve('ok');
            }
        }, 30);
    });
}

function createUserInput() {
    $('#console').append('<input type="text" class="console-input" id="userInput" autocomplete="off"/>');
    $('#userInput').focus();
    $('#userInput').keypress(function (e) {
        if (e.which == 13) {
            username = InputSanitizor($('#userInput').val());
            console.log(username + " submit");
            $('#userInput').prop('readonly', true);
            $.post('/user', JSON.stringify({"username":username}), runHome);
        }
    })
}

function renderMsg(msg){
    Typer.init(msg);
    return new Promise((resolve, reject) => {
        var timer = setInterval(() => {
            Typer.addText({ keyCode: 123748 });

            if (Typer.index > Typer.text.length) {
                clearInterval(timer);
                if (DEBUG) console.log('OK-3');
                resolve('ok');
            }
        }, 30);
    });
}

async function start() {
    await BootUp();
    await UserLogin();
    createUserInput();
    $(document).keypress(function(e){
        if(e.key === "Escape"){
            $('commandInput').val('');
            document.getElementById('commandDiv').hidden = false;
            $('commandInput').focus();
        }
    })
}

function InputSanitizor(data){
    return data.replace(/</gi, '&lt;').replace(/>/gi, '&gt;');
}

var breakline='';

function createCommandField(){
    $( '<div id="commandDiv"><span class="red">'+username+'@PaxPrz:</span>:<span class="blue">~</span>$ <input type="text" class="console-input" id="commandInput" autocomplete="off" /></div>' ).insertAfter('#console');
    $('#commandInput').keypress(function (e) {
        if (e.which == 13) {
            command = InputSanitizor($('#commandInput').val());
            console.log("command: ",command);

            var line = $('#console').html();
            if (line.substring(line.length-15, line.length).includes('table')){
                breakline='';
            }
            if (line.substring(line.length-10, line.length).includes('<br>')){
                breakline='';
            }
            $('#console').append(breakline+'<span class="red">'+username+'@PaxPrz:</span>:<span class="blue">~</span>$ '+command+'<br>');
            // $('#userInput').prop('readonly', true);
            // $('#commandDiv').prop('hidden','true');
            document.getElementById('commandDiv').hidden = true;
            breakline='<br>';
            command = $.trim(command)
            if(command=='clear'){
                $('#console').empty();
                $('#commandInput').val('');
                document.getElementById('commandDiv').hidden = false;
                $(document).scrollTop(0);
                $('#commandInput').focus();
                breakline='';
                return;
            }
            if(command=='matrix'){
                matrix_function();
                $('#commandInput').val('');
                document.getElementById('commandDiv').hidden = false;
                $('#commandInput').focus();
                breakline='';
                $(document).scrollTop($(document).height());
                return;
            }
            if(command==''){
                document.getElementById('commandDiv').hidden = false;
                $('#commandInput').focus();
                breakline='';
                $(document).scrollTop($(document).height());
                return;
            }
            $.post('/command', JSON.stringify({"username":username, "command":command}), addOutput);
        }
    })
    $(document).click(function(){
        $('#commandInput').focus();
    })
    $('#commandInput').focus();    
}

async function runHome(data, status){
    if(status=="success"){
        $('#console').empty();
        // $('#console').append('<span class="red">{0}@PaxPrz:</span>:<span class="blue">~</span>$ ');
        await renderMsg(data['msg']);
        createCommandField();
    }
}

async function addOutput(data, status){
    if(status=="success"){
        $('#console').append(data['msg']);
        
    }else{
        $('#console').append('<span class="error">Backend server response Unsuccessful</span><br>')
    }
    $('#commandInput').val('');
    // $('#commandDiv').removeattr('disabled');
    document.getElementById('commandDiv').hidden = false;
    $(document).scrollTop($(document).height());
    $('#commandInput').focus();
}

start();
