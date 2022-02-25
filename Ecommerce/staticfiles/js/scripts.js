var updateBtns = document.getElementsByClassName('update-cart');
      
      for (var i = 0; i < updateBtns.length; i++) {
          updateBtns[i].addEventListener('click', function() {
              var productId = this.dataset.product;
              var action = this.dataset.action;
              console.log('productId:', productId, 'action:', action);
      
              console.log('USER:', user)
      
              if(user === "AnonymousUser") {
                console.log('Not logged in.')
              }else {
                updateUserCart(productId, action)
              }
          })
      }

      function updateUserCart(product_id, action) {
        console.log('User is authenticated, sending data...')

        var url = '/updateProduct/'

        fetch(url, {
          method:'POST',
          headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
          },
          body:JSON.stringify({'productId': product_id, 'action': action}) 
        })
        
        .then((response) =>{
          return response.json()
        })

        .then((data) =>{
          console.log('data:', data)
          location.reload()
        })

        .catch( () =>{
          console.log('Error')
        })
      }


// function showSearch() {
//   var search = document.getElementsByClassName('search');
//   var icon  = document.getElementsByClassName('search-icon');
  
//   search.setAttribute('class', 'showSearch');
//   icon.style.visibility = 'hidden';
// }