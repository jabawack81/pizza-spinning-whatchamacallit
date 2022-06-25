import express from 'express';

var Users = [{
  username: process.env.USERNAME,
  password: process.env.PASSWORD
}];

var router = express.Router();

router.get('/', function(req, res){
   res.render('login');
});

router.post('/', function(req, res){
   console.log(Users);
   console.log(req.body);
   if(!req.body.username || !req.body.password){
      res.render('login', {message: "Please enter both username and password"});
   } else {
      Users.filter(function(user){
         console.log(user)
         if(user.username === req.body.username && user.password === req.body.password){
            req.session.user = user;
            res.redirect('..');
         }
      });
      res.render('login', {message: "Invalid credentials!"});
   }
});

export default router;