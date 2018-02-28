//
//  LoginViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Alex A on 2/23/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class LoginViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */
    //
    //  ViewController.swift
    //  Music-Driven-Workout-App
    //
    //  Created by Alex A on 2/8/18.
    //  Copyright © 2018 UChicago SoftCon. All rights reserved.
    //
    
    @IBOutlet weak var userBox: UITextField!
    @IBOutlet weak var passBox: UITextField!
    @IBOutlet weak var goButton: UIButton!
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        /* Empty Login Box Check */
        if (userBox.text?.isEmpty)! {
            print("ERR: No userid given.")
            return
        }
        if segue.destination is MenuViewController {
            let vc = segue.destination as? MenuViewController
                vc?.userid = userBox.text!
        }
    }
    
    @IBAction func goButtonClick(_ sender: Any) {
        self.performSegue(withIdentifier: "loginSegue", sender: self)
    }
}
