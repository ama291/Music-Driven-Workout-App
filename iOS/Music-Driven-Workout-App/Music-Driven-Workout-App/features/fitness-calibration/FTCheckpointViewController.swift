//
//  FTCheckpointViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class FTCheckpointViewController: UIViewController {
    
    var userid: String!
    var exid: Int!
    var frequency: Float!
    var isTracked: Bool!
    var exercise: [String:Any] = [String:Any]()
    
    @IBOutlet weak var trackButton: UIButton!
    @IBAction func track(_ sender: UIButton) {
        print("track pressed")
    }
    
    @IBOutlet weak var rateLabel: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        frequency = 90.5
        rateLabel.text = "\(String(Int(frequency))) RPM"
        
        isTracked = false
        let trackedText = isTracked ? "Track Exercise" : "Un-track Exercise"
        print(trackedText)
        
        trackButton.setTitle(trackedText, for: .normal)

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
