
<!DOCTYPE html>
<html lang="en">
  <head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
  <script src="qrc:///qtwebchannel/qwebchannel.js"></script>

  <script type="text/javascript">
  $('document').ready(function(){
      payWithPaystack()
  });
  
    var backend;
      new QWebChannel(qt.webChannelTransport, function(channel){
        backend=channel.objects.backend;
      })

   function payWithPaystack(){
    var handler = PaystackPop.setup({
      key: 'sk_test_117b7e9d5506',
      email: 'customer@email.com',
      amount: 10000,
      currency: "NGN",
      ref: ''+Math.floor((Math.random() * 1000000000) + 1), // generates a pseudo-unique reference. Please replace with a reference you generated. Or remove the line entirely so our API will generate one for you
      firstname: 'Stephen',
      lastname: 'King',
      // label: "Optional string that replaces customer email"
      metadata: {
         custom_fields: [
            {
                display_name: "Mobile Number",
                variable_name: "mobile_number",
                value: "+2348012345678"
            }
         ]
      },
      callback: function(response){
          alert('success. transaction ref is ' + response.reference);
           backend.BackendFunction("Testing");
      },
      onClose: function(){
          alert('window closed');
      }
    });
    handler.openIframe();
  }

     
       
  </script>
  
  </head>
  <body>
  <form >
  <script src="https://js.paystack.co/v1/inline.js"></script>
  <button type="button" onclick="payWithPaystack()"> Pay </button> 
  </form>
  </body>
</html>