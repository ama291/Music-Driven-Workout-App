//
//  FTExerciseViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class FTExerciseViewController: UIViewController {
    
    var userid: String!
    var exerciseName: String!
    var numExercises: Int!
    var exerciseNum: Int!
    var isCalibration: Bool!
    weak var timer: Timer?
    var time: Int = 0
    
    @IBOutlet weak var exName: UILabel!
    @IBOutlet weak var seconds_remaining: UILabel!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.timer = Timer.scheduledTimer(timeInterval: 1.1,
                                          target: self,
                                          selector: #selector(self.advanceTimer(timer:)),
                                          userInfo: nil,
                                          repeats: true)
        // Do any additional setup after loading the view.
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    @objc func advanceTimer(timer: Timer) {
        self.time += 1
        let timeString = String(60 - self.time)
        self.seconds_remaining.text = timeString
        if (self.time == 60) {
            timer.invalidate()
            self.timer = nil
            performSegue(withIdentifier: "to_test_complete", sender: nil)
        }
    }
    
    
    
    @IBAction func complete_test(_ sender: Any) {
    }
    
    // MARK: - Navigation
    
    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        if segue.destination is FTExDescViewController
        {
            let vc = segue.destination as? FTCompleteViewController
            //data to send
            vc?.exerciseName = self.exerciseName
            vc?.isCalibration = self.isCalibration
        }
        
    }
    
}

