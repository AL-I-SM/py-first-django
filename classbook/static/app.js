new Vue({
      el: '#pupils_vue',
      data: {
      pupils: []
      },
      created: function() {
        const vm=this;
        axios.get('/classbook/pupils/api/')
        .then(function(response){
        vm.pupils = response.data
        })
    }
    }
  )

