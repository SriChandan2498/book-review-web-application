function searchbook(event){
    let x=document.forms["search"]["books"].value;
    let y=document.forms["search"]["searchname"].value;
    document.getElementById("tableheader").innerHTML = x
    console.log(x)
    console.log(y)

    var formdata = new FormData();
    formdata.append("books", x);
    formdata.append("searchname", y);
    
    var requestOptions = {
    method: 'POST',
    body: formdata,
    redirect: 'follow'
    };

    fetch("/api/search", requestOptions)
    .then(response => response.text())
    .then((result)=> {
        // console.log(result) 
    books_display=JSON.parse(result)
    // console.log(books_display)
    
    if(books_display === [])
    {
        document.getElementsByTagName("tbody")[0].innerHTML="<tr><td>No "+x+" found</td></tr>"
    }
    else{
        let text=""
        for (let book in books_display){
        // console.log(books_display[book])
        // console.log(text)
            text=text+"<tr><td id = 'booktuple' onclick='getbookdetails()'>"+books_display[book][x]+"</td></tr>"
        }
        // console.log(text)
        document.getElementsByTagName("tbody")[0].innerHTML=text}})
    .catch(error => console.log('error', error));
}

function getbookdetails()
{
    var x = document.querySelector("#booktuple").innerHTML
    // console.log(x)
    fetch("/api/book_details/"+x)
    .then(response => response.text())
    .then((result) =>
    {
        console.log(result)
        details = JSON.parse(result)
        document.querySelector('#bookdetils').innerHTML = '<h4>Details</h4><br>'
                                                          +'<p>Title : '+ details.title+'</p><br>'
                                                          +'<p>Author : '+details.author+'</p><br>'
                                                          +'<p>Published year :'+details.year+'</p><br>'
                                                          +'<p>ISBN :' +details.isbn+'</p><br>'
    })
    .catch(error => console.log('error', error));
}
