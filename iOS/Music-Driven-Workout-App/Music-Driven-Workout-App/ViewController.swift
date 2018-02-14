//
//  ViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Alex A on 2/8/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    @IBAction func exerciseTestClicked(_ sender: Any) {
        performSegue(withIdentifier: "exerciseSegue", sender: self)
    }
    
}

