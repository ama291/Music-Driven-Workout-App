//
//  HeartRateTest.swift
//  Music-Driven-Workout-App
//
//  Created by Gregory Howlett-Gomez on 2/22/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit
import CoreMotion

class ExerciseViewController: UIViewController {
    
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
    
    var motionManager = CMMotionManager()
    var motionData: [[String : Double]] = []
    var timer = Timer()
    var frequency = ""
    
    
    @IBOutlet weak var statusLabel: UILabel!
    @IBOutlet weak var frequencyLabel: UILabel!
    
    func getMotionData() {
        self.statusLabel.text = "collecting data..."
        // saving acceleration every 0.1 seconds
        timer = Timer.scheduledTimer(timeInterval: 30, target: self, selector: #selector(ExerciseViewController.displayResult), userInfo: nil, repeats: false)
        
        var dispTime = -0.1;
        motionManager.accelerometerUpdateInterval = 0.1
        motionManager.startAccelerometerUpdates(to: OperationQueue.current!) {(data, error) in
            if let myData = data
            {
                dispTime += 0.1
                self.statusLabel.text = "collecting data..." + String(format:"%.1f", dispTime) + "s"
                var myDict: [String: Double] = [:]
                myDict = ["xAccl": myData.acceleration.x, "yAccl": myData.acceleration.y, "zAccl": myData.acceleration.z, "timestamp": myData.timestamp]
                
                self.motionData.append(myDict)
            }
        }
    }
    
    //json request struct
    struct jsonRequest: Codable {
        var Result: Float
        var Status: String
    }
    
    @objc func withinTargetHeartRate(heartRate: int, birthyear: int) {
        age = 2018 - birthyear
        heart_rate_base = 220 - age
        min_heart_rate = heart_rate_base * 0.50
        max_heart_rate = heart_rate_base * 0.85
        if (heartRate < max_heart_rate || heartRate > min_heart_rate) {
            return true
        } else {
            return false
        }
    }
    
    @objc func updateLabel() {
        //need to fix this to callback
        self.frequencyLabel.text = self.frequency
    }
    
}

