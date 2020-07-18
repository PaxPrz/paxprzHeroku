var c = document.getElementById("c");
var ctx = c.getContext("2d");

//making the canvas full screen
c.height = window.innerHeight;
c.width = window.innerWidth;

//characters
var charact = "0123456789+-_{}[]!@#$%^&*()=\||\/?>,<.;:";

//converting the string into an array of single characters
charact = charact.split("");

var font_size = 10;
var columns = c.width/font_size; //number of columns for the rain

//an array of drops - one per column
var drops = [];


//x below is the x coordinate
//1 = y co-ordinate of the drop(same for every drop initially)
for(var x = 0; x < columns; x++)
	drops[x] = 1; 

//drawing the characters
function draw()
{

    c.style.top = window.pageYOffset+'px';
    // c.height = window.innerHeight; 
	//Black BG for the canvas
    //translucent BG to show trail
    if (is_running){

        ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
        ctx.fillRect(0, 0, c.width, c.height);
        
        ctx.fillStyle = "#0F0"; //green text
        ctx.font = font_size + "px arial";
        
        //looping over drops
        for(var i = 0; i < drops.length; i++)
        {
            //a random  character to print
            var text = charact[Math.floor(Math.random()*charact.length)];
            
            //x = i*font_size, y = value of drops[i]*font_size
            ctx.fillText(text, i*font_size, drops[i]*font_size);
            
            //sending the drop back to the top randomly after it has crossed the screen
            //adding a randomness to the reset to make the drops scattered on the Y axis
            if(drops[i]*font_size > c.height && Math.random() > 0.975)
                drops[i] = 0;
            
            //incrementing Y coordinate
            drops[i]++;
        }
    }
    if (was_running){
        ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
        ctx.fillRect(0, 0, c.width, c.height);
        
        ctx.fillStyle = "#0F0"; //green text
        ctx.font = font_size + "px arial";
    }
}

var matrix_interval = setInterval(draw, 33);
var is_running = false;
var was_running = false;

function matrix_function(){
    if (is_running){
        console.log("Matrix OFF");
        is_running = false;
        was_running = true;
    }
    else{
        console.log("MATRIX ON");
        is_running = true;
    }
};