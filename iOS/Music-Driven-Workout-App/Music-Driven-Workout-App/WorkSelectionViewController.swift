//
//  WorkSelectionViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class WorkSelectionViewController: UIViewController {
    
    var userid: String!

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        
        populateUI()
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
    @IBOutlet weak var categorymuscle: UITableView!
    
    struct jsonResult: Codable {
        var Result: String
        var Status: String
    }
    
    @objc func populateUI() {
        guard let url = URL(string: "http://138.197.49.155:8000/api/fitness/getcategories/") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let postString = "key=SoftCon2018"
        request.httpBody = postString.data(using: String.Encoding.utf8)
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            if let data = data {
                guard let json = try? JSONDecoder().decode(jsonResult.self, from: data) else { return }
                DispatchQueue.main.async {
                    print(json.Result)
                }
            }
            
        }.resume()
    }
}
