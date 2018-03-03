//
//  CECompleteViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class CECompleteViewController: UIViewController {
    let request = APIRequest()
    var exName: String!
    var exerciseInfo: [String:Any] = [:]
    var freq: Float!
    
    func dateToString(givenDate: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
        let res = formatter.string(from: Date())
        return res
    }
    
    @IBOutlet weak var exerciseName: UILabel!
    @IBOutlet weak var results: UILabel!
    @IBOutlet weak var paceSaved: UILabel!
    @IBAction func savePace(_ sender: Any) {
        let time = self.dateToString(givenDate: Date())
        let qstr = "userid=\(global.userid!)&exid=\(exerciseInfo["id"]!)&rate=\(Int(freq!))&timestamp=\(time)&key=SoftCon2018"
        self.request.submitPostServer(route: "/api/fitness/addexact/", qstring: qstr){(data, response, error) in
            if let error = error {
                fatalError(error.localizedDescription)
            } else {
                let res = self.request.parseJsonInitial(data: data!)
                print(res as Any)
                if res! == "True" {
                    DispatchQueue.main.async {
                        print("Pace saved!")
                        self.paceSaved.text = "Pace saved!"
                    }
                }
            }
            }.resume()
        self.goToHome("")
    }
    @IBAction func tryAgain(_ sender: UIButton) {
        self.performSegue(withIdentifier: "tryAgain", sender: sender)
    }
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        print("user: \(global.userid)")
        print(self.exName)
        print(self.freq)
        print("")

        self.exerciseName.text = self.exName
        self.results.text = "\(self.freq!) RPM"
        self.paceSaved.text = ""

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /* Navigation */
    @IBAction func goToHome(_ sender: Any) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
        present(vc, animated: true, completion: nil)
    }
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.destination is FTExDescViewController
        {
            let vc = segue.destination as? FTExDescViewController
            //data to send
            vc?.exerciseInfo = exerciseInfo
            vc?.isCalibration = true
        }
    }
    
}
