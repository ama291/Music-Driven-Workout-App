//
//  ThemeViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Lucy Newman on 3/3/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class ThemeViewController: UIViewController {
    
    @IBOutlet weak var themeNameLabel: UILabel!
    @IBOutlet weak var numWorkoutsLabel: UILabel!
    
    @IBAction func deleteTheme(_ sender: Any) {
    }
    
    var selectedTheme: [String:Any]!
    var theme: String! = "theme"
    var numWorkouts: String! = "5"
    var userid: String!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        print(self.selectedTheme)
        if selectedTheme == nil {
            return
        }
        self.theme = String(describing: selectedTheme!["name"]!)
        self.numWorkouts = String(describing: selectedTheme!["numworkouts"]!)
        self.themeNameLabel.text = self.theme
        self.numWorkoutsLabel.text = "\(self.numWorkouts!) workouts"
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

}
