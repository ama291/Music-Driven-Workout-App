# Sending Data Through A Segue
```override func prepare(for segue: UIStoryboardSegue, sender: Any?)
    {
        if segue.destination is MenuViewController
        {
            let vc = segue.destination as? MenuViewController\
            //data to send
            vc?.userid = userBox.text!
        }
    }
    
    @IBAction func goButtonClick(_ sender: Any) {
        self.performSegue(withIdentifier: "loginSegue", sender: self)
    }```
