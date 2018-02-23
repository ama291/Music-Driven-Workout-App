//
//  HeartrateTest.swift
//  Music-Driven-Workout-App
//
//  Created by Gregory Howlett-Gomez on 2/22/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit
import CoreMotion

class HeartRateViewController: UIViewController {
    
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
    
    @IBAction func exerciseBack(_ sender: Any) {
        performSegue(withIdentifier: "exerciseBackSegue", sender: self)
    }
    
    @IBOutlet weak var statusLabel: UILabel!
    
    func withinTargetHeartRate(heartRate: Double, birthyear: Int) -> Bool{
        let age = 2018 - birthyear
        let heart_base = 220 - age
        let min_heart_rate = Double(heart_base) * 0.50
        let max_heart_rate = Double(heart_base) * 0.85
        if (heartRate >= min_heart_rate && heartRate <= max_heart_rate) {
            return true
        } else {
            return false
        }
    }
    
    func test_targetheartrate() {
        assert(withinTargetHeartRate(heartRate: 120.5, birthyear: 1977))
        assert(!withinTargetHeartRate(heartRate: 50, birthyear: 1980))
        assert(withinTargetHeartRate(heartRate: 85, birthyear: 1967))
        assert(withinTargetHeartRate(heartRate: 153, birthyear: 1977))
        self.statusLabel.text = "All sample tests have passed"
    }
    
}
