//
//  ProfileViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/26/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class ProfileViewController: UIViewController {
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /* Navigation */
    @IBAction func goToHome(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
        present(vc, animated: true, completion: nil)
    }
    
}
